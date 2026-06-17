from ingestion.connectors.government_connectors import (
    AadhaarConnector, PANConnector, PassportConnector, 
    ElectionConnector, PMKisanConnector, RTIConnector
)
from loguru import logger

def run_ingestion():
    connectors = [
        AadhaarConnector(),
        PANConnector(),
        PassportConnector(),
        ElectionConnector(),
        PMKisanConnector(),
        RTIConnector()
    ]
    
    total_chunks = 0
    for connector in connectors:
        logger.info(f"Running connector: {connector.name}")
        total_chunks += connector.crawl()
        
    logger.info(f"Production ingestion complete. Total chunks: {total_chunks}")

if __name__ == "__main__":
    run_ingestion()
