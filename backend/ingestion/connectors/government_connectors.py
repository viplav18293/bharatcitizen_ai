from ingestion.utils.base_connector import BaseConnector

class AadhaarConnector(BaseConnector):
    def __init__(self):
        urls = [
            "https://uidai.gov.in/en/my-aadhaar/about-your-aadhaar.html",
            "https://uidai.gov.in/en/my-aadhaar/aadhaar-enrolment.html",
            "https://uidai.gov.in/en/my-aadhaar/update-aadhaar.html"
        ]
        super().__init__("UIDAI", urls, "aadhaar")

class PANConnector(BaseConnector):
    def __init__(self):
        urls = [
            "https://www.incometax.gov.in/iec/foportal/help/permanent-account-number",
            "https://www.incometax.gov.in/iec/foportal/help/pan-correction"
        ]
        super().__init__("IncomeTax", urls, "pan")

class PassportConnector(BaseConnector):
    def __init__(self):
        urls = [
            "https://www.passportindia.gov.in/AppClientProject/online/faqMain"
        ]
        super().__init__("PassportSeva", urls, "passport")

class ElectionConnector(BaseConnector):
    def __init__(self):
        urls = [
            "https://eci.gov.in/faqs/voter/registration-and-correction/"
        ]
        super().__init__("ECI", urls, "voterid")

class PMKisanConnector(BaseConnector):
    def __init__(self):
        urls = [
            "https://pmkisan.gov.in/FAQ.aspx"
        ]
        super().__init__("PMKisan", urls, "pm_kisan")

class RTIConnector(BaseConnector):
    def __init__(self):
        urls = [
            "https://rti.gov.in/rti-act.php"
        ]
        super().__init__("RTI", urls, "rti")
