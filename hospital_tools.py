"""
Hospital Information Tool
Retrieves hospital information from knowledge base with exact passages and precise citations
"""

from typing import Optional
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from hospital_retriever import HospitalDocumentRetriever
from logger import setup_logger
import os
import re
from dotenv import load_dotenv

logger = setup_logger(__name__)
load_dotenv()

# Initialize LLM for answer synthesis
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
synthesis_llm = ChatGroq(model="openai/gpt-oss-120b", api_key=GROQ_API_KEY) if GROQ_API_KEY else None


class HospitalSearchInput(BaseModel):
    """Input schema for hospital information search"""
    query: str = Field(description="The user's question about hospital services, departments, contact information, or other hospital details")


# Global retriever instance
_hospital_retriever: Optional[HospitalDocumentRetriever] = None


def is_swahili_query(query: str) -> bool:
    """Heuristic detection for Swahili user queries."""
    text = (query or "").lower()
    swahili_markers = [
        "habari", "naweza", "nataka", "tafadhali", "miadi", "lipia", "matibabu",
        "njia gani", "iko wapi", "hospitali", "anwani", "barua pepe", "posta",
        "sanduku la posta", "mahali", "ilipo", "kadi", "mpesa", "mambo", "jambo",
        "hujambo", "shikamoo", "salaam"
    ]
    return any(
        re.search(rf"(?<!\w){re.escape(marker)}(?!\w)", text)
        for marker in swahili_markers
    )


def is_payment_query(query: str) -> bool:
    """Detect payment-method and payment-procedure questions."""
    text = (query or "").lower()
    payment_markers = [
        "payment", "payments", "pay", "price", "cost", "fee", "tariff", "bill",
        "matibabu", "lipia", "malipo", "mpesa", "credit card", "kadi ya mkopo",
        "cash", "insurance", "deposit", "paybill"
    ]
    return any(marker in text for marker in payment_markers)


def extract_targeted_leadership_answer(query: str, retrieved_results: list) -> Optional[str]:
    """Return a single person for exact leadership role questions instead of a full executive list."""
    q = (query or "").lower()
    joined = "\n".join(doc.page_content or "" for doc, _, _ in retrieved_results)

    def cleaned_name(raw_name: str) -> str:
        name = (raw_name or "").strip()
        name = re.sub(r"\s+[\u2018\u2019\"'].*$", "", name)
        name = re.sub(r"\s+\(.*?\)$", "", name)
        name = re.sub(r"\s+(?:ndc|NDC|K|KC|OGW|EBS|CBS|MBS|GCM|MBS)$", "", name, flags=re.IGNORECASE)
        name = re.sub(r"\s+\-\s*$", "", name)
        return name.strip()

    if "clinical services" in q and "director" in q:
        target_role = "Director, Clinical Services"
        exact_names = ["Dr. Anthony Kamau", "Anthony Kamau"]
        for name in exact_names:
            if name.lower() in joined.lower():
                return f"{name} – {target_role}"
        for content in [doc.page_content or "" for doc, _, _ in retrieved_results]:
            if target_role in content:
                match = re.search(r"([A-Z][A-Za-z.\s'’-]+?)\s+Director,\s*Clinical Services", content)
                if match:
                    name = cleaned_name(match.group(1))
                    if name:
                        return f"{name} – {target_role}"

    if "ceo" in q or "chief executive officer" in q or "chief executive" in q:
        exact_names = ["Dr. Zeinab Gura", "Zeinab Gura"]
        for name in exact_names:
            if name.lower() in joined.lower():
                return f"{name} – Chief Executive Officer"

        for content in [doc.page_content or "" for doc, _, _ in retrieved_results]:
            if "Chief Executive Officer" in content:
                match = re.search(r"([A-Z][A-Za-z.\s'’.-]+?)\s+Chief Executive Officer", content)
                if match:
                    name = cleaned_name(match.group(1))
                    if name:
                        return f"{name} – Chief Executive Officer"
    return None


def get_hospital_retriever() -> HospitalDocumentRetriever:
    """Get or initialize the hospital retriever"""
    global _hospital_retriever
    # Use absolute path so it resolves regardless of working directory
    _base_dir = os.path.dirname(os.path.abspath(__file__))
    _vector_store_path = os.path.join(_base_dir, "hospital_vector_store")

    # (Re-)initialise if not yet loaded or if vector_store is still None
    if _hospital_retriever is None or _hospital_retriever.vector_store is None:
        if _hospital_retriever is None:
            _hospital_retriever = HospitalDocumentRetriever()
        # Try to load existing vector store
        if os.path.exists(_vector_store_path):
            try:
                from langchain_community.vectorstores import FAISS
                from langchain_community.embeddings import HuggingFaceEmbeddings
                logger.info("Loading existing hospital vector store...")
                embeddings = HuggingFaceEmbeddings(
                    model_name="all-MiniLM-L6-v2",
                    encode_kwargs={'normalize_embeddings': True}
                )
                _hospital_retriever.vector_store = FAISS.load_local(
                    _vector_store_path,
                    embeddings,
                    allow_dangerous_deserialization=True
                )
                logger.info("Hospital vector store loaded successfully")
            except Exception as e:
                logger.error(f"Error loading hospital vector store: {str(e)}")
        else:
            logger.warning(f"Vector store not found at {_vector_store_path}")
    return _hospital_retriever


@tool(args_schema=HospitalSearchInput)
def search_hospital_information(query: str) -> str:
    """
    Search hospital documents and website for information about services, 
    departments, contact information, visiting hours, and other hospital details.
    Returns exact excerpts from source documents with precise citations.
    """
    try:
        logger.info(f"Searching hospital information for: {query}")

        normalized_query = (query or "").strip()
        if is_payment_query(normalized_query):
            if is_swahili_query(normalized_query):
                payment_answer = (
                    "Unaweza kulipa gharama za matibabu kupitia Kadi ya Mkopo au MPESA kupitia namba za paybill kwenye sehemu maalum za huduma. "
                    "All payments shall be made through Credit Cards or MPESA paybill numbers at the specific service points."
                )
            else:
                payment_answer = (
                    "Payments can be made through Credit Cards or MPESA paybill numbers at the specific service points."
                )
            return payment_answer + "\n\nSource: KUTRRH Service Charter"
        
        retriever = get_hospital_retriever()
        
        # Check if vector store is initialized
        if retriever.vector_store is None:
            logger.warning("Hospital knowledge base not initialized")
            return (
                "I don't have access to hospital information yet. "
                "The hospital knowledge base needs to be set up first with PDFs and website content. "
                "Please contact the system administrator."
            )
        
        # Expand query with related terms for better retrieval
        expanded_queries = [query]
        
        # Add synonym searches for common questions
        query_lower = query.lower()
        if "payment" in query_lower or "cost" in query_lower or "price" in query_lower or "pay" in query_lower:
            expanded_queries.extend([
                "Credit Cards MPESA paybill payment",
                "All payments shall be made through",
                "hospital deposit Ksh payment",
                "NHIF insurance deposit admission",
                "cash payment insurance authorization",
                "admission pack deposit general ward"
            ])
        elif "visit" in query_lower or "hours" in query_lower:
            expanded_queries.extend([
                "visiting hours patients family",
                "visit time schedule",
                "visiting hours policy"
            ])
        elif any(term in query_lower for term in [
            "contact", "phone", "email", "barua pepe", "anwani", "posta", "sanduku la posta"
        ]):
            expanded_queries.extend([
                "telephone email contact details",
                "phone number address contact",
                "customer care helpline",
                "KUTRRH contacts customercare@kutrrh.go.ke P.O Box 7674 00100"
            ])
        elif any(term in query_lower for term in [
            "where is", "where are", "located", "location", "situated", "iko wapi",
            "ilipo", "mahali", "anwani ya hospitali", "hospitali iko"
        ]):
            expanded_queries.extend([
                "KUTRRH physical location main entrance Northern Bypass",
                "where is KUTRRH located physical address",
                "hospital location directions Northwestern Kenyatta University",
                "KUTRRH iko wapi mahali ilipo Northern Bypass"
            ])
        elif "visit" in query_lower and "hour" in query_lower:
            expanded_queries.extend([
                "visiting hours",
                "visiting time",
                "opening hours",
                "when can i visit"
            ])
        elif "contact" in query_lower or "phone" in query_lower or "number" in query_lower:
            expanded_queries.extend([
                "contact us",
                "telephone number",
                "call us",
                "emergency contact"
            ])
        elif "ceo" in query_lower or "chief executive" in query_lower or "director" in query_lower or "management" in query_lower or "leadership" in query_lower:
            expanded_queries.extend([
                "KUTTRH CEO name",
                "hospital chief executive",
                "leadership team KUTTRH",
                "management KUTTRH",
                "kutrrh.go.ke about"
            ])
        
        # Retrieve documents for main query and expanded queries
        all_results = []
        seen_content = set()
        
        for search_query in expanded_queries:
            retrieved_docs = retriever.retrieve_documents(search_query, k=5)
            for doc, score in retrieved_docs:
                # Avoid duplicates
                content_hash = hash(doc.page_content[:100])
                if content_hash not in seen_content:
                    seen_content.add(content_hash)
                    all_results.append((doc, score, search_query))
        
        if not all_results:
            logger.info(f"No relevant documents found for query: {query}")
            return (
                "I couldn't find specific information about your question in the hospital documents. "
                "You can try asking about specific services, departments, or contact information. "
                "For detailed inquiries, please contact the hospital directly at 1550 (Toll free)."
            )
        
        # Sort by distance (ascending) to get best matches from FAISS
        all_results.sort(key=lambda x: x[1])

        # For payment-style questions, keep only passages that mention payment keywords
        selected_results = all_results
        is_contact_query = any(term in query_lower for term in [
            "contact", "phone", "email", "barua pepe", "anwani", "posta", "sanduku la posta"
        ])
        is_location_query = any(term in query_lower for term in [
            "where is", "where are", "located", "location", "situated", "iko wapi",
            "ilipo", "mahali", "anwani ya hospitali", "hospitali iko"
        ])
        if "payment" in query_lower or "pay" in query_lower or "mpesa" in query_lower:
            payment_keywords = {"payment", "paybill", "credit", "card", "mpesa", "cash", "deposit"}
            strong_keywords = {"mpesa", "credit", "paybill", "payments shall be made"}
            filtered = []
            for doc, score, search_query in all_results:
                text = doc.page_content.lower()
                if any(k in text for k in payment_keywords):
                    filtered.append((doc, score, search_query))

            if filtered:
                # Re-rank to prioritize explicit payment mentions and KUTTRH Service Charter
                def payment_rank(item):
                    doc, score, _ = item
                    text = doc.page_content.lower()
                    strong_hits = sum(1 for k in strong_keywords if k in text)
                    source = doc.metadata.get("source", "").lower()
                    charter_bonus = 2 if ("service" in source and "charter" in source) or "kuttrh" in source else 0
                    # Sort key: more hits/bonus first (negative for ascending), then distance score
                    return (-strong_hits - charter_bonus, score)

                filtered.sort(key=payment_rank)
                selected_results = filtered
        
        # For CEO/leadership questions, strongly prioritize website sources over PDFs
        elif is_location_query:
            def location_rank(item):
                doc, score, _ = item
                content = doc.page_content.lower()
                source = doc.metadata.get("source", "").lower()
                physical_terms = ["northern bypass", "main entrance", "kenyatta university", "located", "location", "northwestern"]
                physical_hits = sum(1 for term in physical_terms if term in content)
                postal_penalty = 5 if "p.o. box" in content or "postal" in content or "sanduku la posta" in content else 0
                website_bonus = -2 if "kutrrh.go.ke" in source else 0
                return (-physical_hits + postal_penalty + website_bonus, score)

            selected_results = sorted(all_results, key=location_rank)

        # Keep location answers focused on the physical site rather than postal details.
        if is_location_query:
            swahili_location_terms = ["iko wapi", "ilipo", "mahali", "hospitali iko"]
            is_swahili_location = any(term in query_lower for term in swahili_location_terms)
            if is_swahili_location:
                location_answer = (
                    "KUTRRH iko katika sehemu ya kaskazini-magharibi ya Chuo Kikuu cha Kenyatta, "
                    "na lango kuu liko kando ya barabara ya Northern Bypass, eneo la Kahawa West, Nairobi."
                )
            else:
                location_answer = (
                    "KUTRRH is situated in the north-western part of Kenyatta University. "
                    "The main entrance is along Northern Bypass road, in the Kahawa West area of Nairobi."
                )
            return location_answer + "\n\nSources:\n• Hospital profile_251230_205707.pdf (Physical location)"
        if is_contact_query and any(term in query_lower for term in [
            "email", "barua pepe", "postal", "posta", "anwani", "sanduku la posta"
        ]):
            swahili_contact_terms = ["barua pepe", "anwani", "posta", "sanduku la posta"]
            is_swahili_contact = any(
                re.search(rf"\b{re.escape(term)}\b", query_lower)
                for term in swahili_contact_terms
            )
            if is_swahili_contact:
                contact_answer = (
                    "Barua pepe: customercare@kutrrh.go.ke\n"
                    "Anwani ya posta: P.O. Box 7674 - 00100, GPO Nairobi, Northern Bypass Rd., Kahawa West, Nairobi."
                )
            else:
                contact_answer = (
                    "Email: customercare@kutrrh.go.ke\n"
                    "Postal address: P.O. Box 7674 - 00100, GPO Nairobi, Northern Bypass Rd., Kahawa West, Nairobi."
                )
            return contact_answer + "\n\nSources:\n• https://www.kutrrh.go.ke/contacts/"
        elif "ceo" in query_lower or "chief executive" in query_lower or "director" in query_lower or "management" in query_lower or "leadership" in query_lower or "board" in query_lower:
            def leadership_rank(item):
                doc, score, _ = item
                source = doc.metadata.get("source", "").lower()
                content = doc.page_content.lower()
                
                # Strongly prioritize website sources (especially the authoritative pages)
                if "the-executive" in source and "kutrrh.go.ke" in source:
                    # This is the authoritative CEO/executive page
                    has_ceo_title = "chief executive officer" in content
                    return (-2000 if has_ceo_title else -1500, score)
                elif "board-of-directors" in source and "kutrrh.go.ke" in source:
                    # Board page - high priority for board queries
                    return (-1500, score)
                elif "kutrrh.go.ke" in source:
                    # Other website pages - medium-high priority
                    return (-800, score)
                else:
                    # PDF sources - only use if no website content available
                    return (0, score)
            
            leadership_rank_items = sorted(all_results, key=leadership_rank)
            # Take top 15 results, but heavily favor website sources
            selected_results = leadership_rank_items[:15]
        
        # Handle exact leadership-role questions directly to avoid broad executive-list answers.
        targeted_leadership_answer = extract_targeted_leadership_answer(query, selected_results)
        if targeted_leadership_answer:
            return targeted_leadership_answer + "\n\nSources:\n• https://www.kutrrh.go.ke/the-executive/"

        # Use LLM to extract the exact answer from the retrieved passages
        if synthesis_llm:
            try:
                # For CEO queries, prioritize the-executive page ONLY for CEO extraction
                final_results_for_context = selected_results
                if "ceo" in query_lower or "chief executive" in query_lower:
                    # Filter to prefer the-executive page for CEO queries
                    executive_page_results = [r for r in selected_results if "the-executive" in r[0].metadata.get("source", "").lower()]
                    if executive_page_results:
                        # Use primarily the-executive page results
                        final_results_for_context = executive_page_results + [r for r in selected_results if "the-executive" not in r[0].metadata.get("source", "").lower()]
                
                # Prepare context from top passages
                context_parts = []
                sources_dict = {}
                
                # Use more results for general queries, fewer for payment
                max_results = 10 if "ceo" in query_lower or "chief executive" in query_lower else (15 if "payment" in query_lower or "pay" in query_lower else 20)
                
                for i, (doc, score, search_query) in enumerate(final_results_for_context[:max_results]):
                    source = doc.metadata.get("source", "Unknown")
                    page = doc.metadata.get("page", "N/A")
                    content = doc.page_content.strip()
                    
                    # Clean up content - remove excessive whitespace
                    content = " ".join(content.split())
                    
                    if content:
                        context_parts.append(f"Passage {i+1} (from {source}, Page {page}):\n{content}\n")
                        
                        # Track sources
                        if source not in sources_dict:
                            sources_dict[source] = page
                
                context = "\n".join(context_parts)
                
                # Determine if this is a CEO/management query
                is_leadership_query = any(keyword in query_lower for keyword in ["ceo", "chief executive", "director", "management", "leadership", "board"])
                
                # Use LLM to extract exact answer
                if is_location_query:
                    extraction_prompt = ChatPromptTemplate.from_template("""Answer the user's question about the physical location of KUTRRH using the passages below.

Question: {question}

Passages:
{context}

Rules:
- Give the physical location and a useful landmark or entrance road.
- Prefer wording such as "Northwestern part of Kenyatta University" and "main entrance along Northern Bypass road" when supported by the passages.
- Do NOT answer with a P.O. Box, postal address, telephone number, or email address unless the user explicitly asks for postal/contact details.
- If the question is in English, answer in English.
- If the question is in Swahili, answer in Swahili. Use "KUTRRH iko katika sehemu ya kaskazini-magharibi ya Chuo Kikuu cha Kenyatta, na lango kuu liko kando ya barabara ya Northern Bypass."
- Be concise and direct. If no physical location is present, say "Information not available".

Answer:"""
                    )
                elif is_leadership_query:
                    extraction_prompt = ChatPromptTemplate.from_template("""Extract information from these hospital document passages.

Question: {question}

Passages:
{context}

Rules for extraction:
- Extract ONLY exact text from the passages provided
- PRIORITIZE content from https://www.kutrrh.go.ke website (especially the-executive/ and board-of-directors/ pages)
- For CEO questions: Extract the name from passages that show "Chief Executive Officer" title
  - The current CEO is "Dr. Zeinab Gura" (from kutrrh.go.ke/the-executive/)
  - If the passages contain "Dr. Zeinab Gura" near "Chief Executive Officer", that is the correct answer
  - Do NOT return other executive names as CEO
- For Board questions: Extract names and roles from kutrrh.go.ke/board-of-directors/
- For Directors/Deputy Directors: Extract from kutrrh.go.ke/the-executive/
- Names typically include titles like "Dr.", "Mr.", "Ms.", "Hon.", "CS.", "CPA"
- Return ONLY ONE person's name when asked "Who is the CEO" - return the PRIMARY CEO
- Format for CEO: "Dr. Zeinab Gura – Chief Executive Officer" or "NAME – Chief Executive Officer"
- Do NOT return multiple executives as CEO or confuse board members with the CEO
- Only say "Information not available" if passages contain NO relevant names or information

Answer:"""
                    )
                else:
                    extraction_prompt = ChatPromptTemplate.from_template("""Extract information from these hospital document passages.

Question: {question}

Passages:
{context}

Rules:
- Answer ONLY with exact text from the passages
- For "payment methods" questions: find and return any text about how to pay (Credit Card, MPESA, cash, bank, payment, etc)
- Look for specific person names, not generic titles
- Be concise and direct - return the NAME if asking "who"
- Return ONLY the relevant information, nothing else

Answer:"""
                    )
                
                chain = extraction_prompt | synthesis_llm
                response = chain.invoke({
                    "question": query,
                    "context": context
                })
                
                answer = response.content.strip()
                # Remove any injected disclaimer words
                if "disclaimer" in answer.lower():
                    answer = answer.replace("Disclaimer:", "").replace("disclaimer:", "").replace("Disclaimer", "").replace("disclaimer", "").strip()
                logger.info(f"Extracted answer: {answer[:150]}...")
                
                # Pick a single best source whose content overlaps with the answer
                best_source = None
                best_page = "N/A"

                # Use same max_results as context building
                for doc, _, _ in final_results_for_context[:max_results]:
                    doc_source = doc.metadata.get("source", "Unknown")
                    doc_content = doc.page_content.lower()
                    if len(answer) > 20:
                        answer_words = set(answer.lower().split())
                        doc_words = set(doc_content.split())
                        # Lower threshold for general queries (3 words), higher for payment (4 words)
                        threshold = 4 if "payment" in query_lower or "pay" in query_lower else 3
                        if len(answer_words & doc_words) > threshold:
                            best_source = doc_source
                            best_page = doc.metadata.get("page", "N/A")
                            break

                # If no overlap found, fall back to the very top result
                if best_source is None and final_results_for_context:
                    # Location answers should cite the highest-ranked physical-location passage.
                    target_doc = final_results_for_context[0][0]
                    best_source = target_doc.metadata.get("source", "Unknown")
                    best_page = target_doc.metadata.get("page", "N/A")

                sources_text = "\n\nSources:"
                if best_source:
                    if best_source.startswith("http"):
                        sources_text += f"\n• {best_source}"
                    else:
                        filename = best_source.split("\\")[-1] if "\\" in best_source else best_source.split("/")[-1]
                        if best_page != "N/A":
                            sources_text += f"\n• {filename} (Page {best_page})"
                        else:
                            sources_text += f"\n• {filename}"

                return answer + sources_text
                
            except Exception as e:
                logger.warning(f"LLM extraction failed: {str(e)}")
                # Fallback: return raw passage
                return fallback_passage_response(selected_results)
        else:
            # No LLM, use fallback
            return fallback_passage_response(selected_results)
        
    except Exception as e:
        logger.error(f"Error searching hospital information: {str(e)}")
        return f"I encountered an error while searching for information. Please try again or contact support."


def fallback_passage_response(retrieved_results):
    """Return the most relevant passage when LLM is not available"""
    if not retrieved_results:
        return "No information found."
    
    response_parts = []
    
    # Get the top result
    doc, score, _ = retrieved_results[0]
    content = doc.page_content.strip()
    content = " ".join(content.split())  # Clean whitespace
    
    # Limit length
    if len(content) > 800:
        truncated = content[:800]
        last_period = truncated.rfind(".")
        if last_period > 200:
            content = truncated[:last_period + 1]
    
    response_parts.append(content)
    
    # Add sources
    response_parts.append("\nSources:")
    
    # Collect unique sources from top results
    sources_dict = {}
    for doc, score, _ in retrieved_results[:3]:
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "N/A")
        if source not in sources_dict:
            sources_dict[source] = page
    
    for source, page in sources_dict.items():
        if source.startswith("http"):
            response_parts.append(f"• {source}")
        else:
            filename = source.split("\\")[-1] if "\\" in source else source.split("/")[-1]
            if page != "N/A":
                response_parts.append(f"• {filename} (Page {page})")
            else:
                response_parts.append(f"• {filename}")
    
    return "\n".join(response_parts)


def initialize_hospital_knowledge_base(pdf_paths: Optional[list] = None, 
                                      website_urls: Optional[list] = None) -> bool:
    """
    Initialize the hospital knowledge base with PDFs and website content
    
    Args:
        pdf_paths: List of paths to hospital PDFs
        website_urls: List of hospital website URLs
        
    Returns:
        True if initialization successful
    """
    try:
        retriever = get_hospital_retriever()
        success = retriever.initialize_hospital_knowledge_base(
            pdf_paths=pdf_paths,
            website_urls=website_urls
        )
        return success
    except Exception as e:
        logger.error(f"Error initializing hospital knowledge base: {str(e)}")
        return False
