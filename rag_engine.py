# =====================================================
# Population Health RAG Engine
# =====================================================

# Embeddings
from langchain_huggingface import HuggingFaceEmbeddings

# Vector Store
from langchain_community.vectorstores import FAISS

# LLM
from langchain_ollama import ChatOllama



# =====================================================
# LOAD EMBEDDING MODEL
# =====================================================

embedding_model = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)



# =====================================================
# LOAD FAISS VECTOR DATABASE
# =====================================================

vectorstore = FAISS.load_local(
    "C:\\Users\\D882205\\Desktop\\Capstone grp2\\rag\\population_health_index",
    embedding_model,
    allow_dangerous_deserialization=True
)



# =====================================================
# CREATE RETRIEVER
# =====================================================

retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 7,
        "fetch_k": 30
    }
)



# =====================================================
# LOAD LLAMA 3
# =====================================================

llm = ChatOllama(
    model="llama3"
)



# =====================================================
# GENERAL HEALTH CHATBOT
# =====================================================

def ask_health_advisor(question):

    # Retrieve relevant chunks
    docs = retriever.invoke(question)

    # If nothing found
    if not docs:
        return "Information not found in the knowledge base."

    # Build Context
    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    # Prompt
    prompt = f"""
You are an AI Population Health Advisor.

Use ONLY the information present
in the supplied context.

If information is not available,
say:

Information not found in the knowledge base.

--------------------------------------------------
CONTEXT
--------------------------------------------------

{context}

--------------------------------------------------
QUESTION
--------------------------------------------------

{question}

Provide a clear,
healthcare-focused answer.
"""

    # Generate Response
    response = llm.invoke(prompt)

    return response.content



# =====================================================
# PERSONALIZED MEMBER RECOMMENDATION
# =====================================================

def generate_member_recommendation(member):

    # Handle missing cluster values

    cluster = (
        member["Cluster_Name"]
        if str(member["Cluster_Name"]) != "nan"
        else "Unknown"
    )



    # -------------------------------------------------
    # Build Retrieval Query
    # -------------------------------------------------

    query = f"""
Cluster: {cluster}

Age: {member['Age']}

BMI: {member['BMI']}

Blood Glucose: {member['Glucose']}

Smoking Status: {member['Smoking_Status']}

Hypertension:
{member['Existing_Hypertension_Flag']}

Risk Category:
{member['Risk_Category']}

Risk Probability:
{member['Risk_Probability']}

Need:

- clinical recommendations

- wellness program recommendations

- intervention playbooks

- preventive screenings

- care management actions

- business recommendations

- population health interventions
"""



    # -------------------------------------------------
    # Retrieve Relevant Documents
    # -------------------------------------------------

    results = retriever.invoke(query)



    # -------------------------------------------------
    # Filter Noisy Chunks
    # -------------------------------------------------

    filtered_docs = []

    for doc in results:

        text = doc.page_content

        if "Healthy Low-Risk Members" in text:
            continue

        filtered_docs.append(doc)



    # -------------------------------------------------
    # Build Context
    # -------------------------------------------------

    context = "\n\n".join(
        [doc.page_content for doc in filtered_docs]
    )



    # -------------------------------------------------
    # Build Source List
    # -------------------------------------------------

    sources = "\n".join(
        list(
            set(
                doc.metadata.get(
                    "source_file",
                    "Unknown"
                )
                for doc in filtered_docs
            )
        )
    )



    # -------------------------------------------------
    # Prompt
    # -------------------------------------------------

    prompt = f"""
You are an AI Population Health Advisor.

Use ONLY information present
in the retrieved context.

If information is unavailable,
state:

Information not found in the knowledge base.

--------------------------------------------------
MEMBER PROFILE
--------------------------------------------------

Age: {member['Age']}

BMI: {member['BMI']}

Blood Glucose: {member['Glucose']}

Smoking Status: {member['Smoking_Status']}

Hypertension:
{member['Existing_Hypertension_Flag']}

Risk Category:
{member['Risk_Category']}

Risk Probability:
{member['Risk_Probability']}

Cluster:
{cluster}

--------------------------------------------------
RETRIEVED CONTEXT
--------------------------------------------------

{context}

--------------------------------------------------
SOURCES
--------------------------------------------------

{sources}

--------------------------------------------------
TASK
--------------------------------------------------

Generate the response using EXACTLY
this structure.

Risk Summary
-------------

Clinical Recommendations
------------------------

Lifestyle Interventions
-----------------------

Recommended Wellness Programs
-----------------------------

Preventive Screenings
---------------------

Business / Care Management Actions
----------------------------------

Source-Based Reasoning
----------------------

Rules:

1. Use ONLY retrieved context.

2. Do NOT invent programs.

3. Do NOT make assumptions.

4. If information is unavailable,
write:
Information not found in the knowledge base.
"""



    # -------------------------------------------------
    # Generate Final Recommendation
    # -------------------------------------------------

    response = llm.invoke(
        prompt
    )

    return response.content

