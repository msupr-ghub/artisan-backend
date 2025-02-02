from pathlib import Path

from app.dependencies import get_rag_service


async def process_knowledge_base() -> None:
    rag_service = get_rag_service()
    kb_dir = Path(__file__).parent / "app/knowledgebase"

    files = []
    for file_path in kb_dir.rglob("*"):
        if file_path.is_file():
            files.append(str(file_path))

    for file_path in files:
        await rag_service.process_file(file_path)