"""Browser automation for job application forms using Playwright."""

from pathlib import Path
from typing import Optional, List, Dict, Any
from enum import Enum

try:
    from playwright.sync_api import sync_playwright, Page, Browser
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

from src.config_manager import ConfigManager


class AutoFillMode(Enum):
    """Auto-fill modes."""
    SUPERVISED = "supervised"  # Fill one section at a time with confirmation
    SEMI_AUTO = "semi-auto"    # Fill all but pause before submission
    FULL_AUTO = "full-auto"    # Fill everything with final confirmation


class AutoApply:
    """Automates filling of job application forms."""
    
    def __init__(
        self,
        config_manager: Optional[ConfigManager] = None,
        mode: AutoFillMode = AutoFillMode.SUPERVISED,
        headless: bool = False
    ):
        """Initialize the auto-apply bot.
        
        Args:
            config_manager: Config manager instance
            mode: Auto-fill mode
            headless: Run browser in headless mode
        """
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError(
                "Playwright not installed. Run: pip install playwright && playwright install"
            )
        
        self.config = config_manager or ConfigManager()
        self.mode = mode
        self.headless = headless
        self.profile = None
    
    def fill_application(
        self,
        url: str,
        resume_path: Optional[Path] = None,
        cover_letter_path: Optional[Path] = None
    ) -> bool:
        """Fill a job application form.
        
        Args:
            url: Application URL
            resume_path: Path to resume PDF
            cover_letter_path: Path to cover letter PDF
            
        Returns:
            True if successful, False otherwise
        """
        # Load profile
        self.profile = self.config.load_profile()
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            
            try:
                # Navigate to application page
                print(f"Opening {url}...")
                page.goto(url)
                page.wait_for_load_state("networkidle")
                
                # Detect and fill fields
                self._fill_form(page, resume_path, cover_letter_path)
                
                # Handle submission based on mode
                if self.mode == AutoFillMode.SUPERVISED:
                    self._supervised_submit(page)
                elif self.mode == AutoFillMode.SEMI_AUTO:
                    self._semi_auto_submit(page)
                elif self.mode == AutoFillMode.FULL_AUTO:
                    self._full_auto_submit(page)
                
                return True
                
            except Exception as e:
                print(f"Error during auto-fill: {e}")
                return False
            finally:
                if not self.headless:
                    input("\nPress Enter to close browser...")
                browser.close()
    
    def _fill_form(
        self,
        page: Page,
        resume_path: Optional[Path],
        cover_letter_path: Optional[Path]
    ) -> None:
        """Detect and fill form fields.
        
        Args:
            page: Playwright page
            resume_path: Resume file path
            cover_letter_path: Cover letter file path
        """
        personal_info = self.profile["personal_info"]
        address = self.profile.get("address", {})
        
        # Common field patterns
        field_mappings = {
            "first_name": ["first name", "firstname", "fname"],
            "last_name": ["last name", "lastname", "lname"],
            "email": ["email", "e-mail"],
            "phone": ["phone", "telephone", "mobile"],
            "address": ["address", "street"],
            "city": ["city"],
            "state": ["state", "province"],
            "zip": ["zip", "postal", "postcode"],
            "linkedin": ["linkedin"],
            "website": ["website", "portfolio"]
        }
        
        # Extract name parts
        name_parts = personal_info["name"].split()
        first_name = name_parts[0] if name_parts else ""
        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
        
        # Data to fill
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": personal_info.get("email", ""),
            "phone": personal_info.get("phone", ""),
            "address": address.get("street", ""),
            "city": address.get("city", ""),
            "state": address.get("state", ""),
            "zip": address.get("zip", ""),
            "linkedin": self.profile.get("links", {}).get("linkedin", ""),
            "website": self.profile.get("links", {}).get("website", "")
        }
        
        # Fill text fields
        for field_type, patterns in field_mappings.items():
            value = data.get(field_type, "")
            if value:
                self._fill_field_by_patterns(page, patterns, value)
        
        # Handle file uploads
        if resume_path:
            self._upload_file(page, ["resume", "cv"], resume_path)
        
        if cover_letter_path:
            self._upload_file(page, ["cover letter", "coverletter"], cover_letter_path)
        
        # Wait for user in supervised mode
        if self.mode == AutoFillMode.SUPERVISED:
            print("\n✅ Form filled. Review the information.")
            response = input("Press Enter to continue, 's' to skip, or 'e' to edit: ").lower()
            if response == 's':
                raise Exception("User skipped")
    
    def _fill_field_by_patterns(
        self,
        page: Page,
        patterns: List[str],
        value: str
    ) -> bool:
        """Fill a field matching one of the patterns.
        
        Args:
            page: Playwright page
            patterns: List of text patterns to match
            value: Value to fill
            
        Returns:
            True if field was filled
        """
        for pattern in patterns:
            # Try different selectors
            selectors = [
                f'input[name*="{pattern}" i]',
                f'input[id*="{pattern}" i]',
                f'input[placeholder*="{pattern}" i]',
                f'input[aria-label*="{pattern}" i]'
            ]
            
            for selector in selectors:
                try:
                    elements = page.query_selector_all(selector)
                    if elements:
                        elements[0].fill(value)
                        print(f"✓ Filled {pattern}: {value}")
                        return True
                except Exception:
                    continue
        
        return False
    
    def _upload_file(
        self,
        page: Page,
        patterns: List[str],
        file_path: Path
    ) -> bool:
        """Upload a file to a file input.
        
        Args:
            page: Playwright page
            patterns: Text patterns to match
            file_path: File to upload
            
        Returns:
            True if file was uploaded
        """
        for pattern in patterns:
            selectors = [
                f'input[type="file"][name*="{pattern}" i]',
                f'input[type="file"][id*="{pattern}" i]',
                f'input[type="file"][aria-label*="{pattern}" i]'
            ]
            
            for selector in selectors:
                try:
                    elements = page.query_selector_all(selector)
                    if elements:
                        elements[0].set_input_files(str(file_path))
                        print(f"✓ Uploaded {pattern}: {file_path.name}")
                        return True
                except Exception:
                    continue
        
        return False
    
    def _supervised_submit(self, page: Page) -> None:
        """Handle submission in supervised mode."""
        print("\n📋 Review the application before submitting.")
        print("Would you like to submit?")
        response = input("Type 'yes' to submit, anything else to cancel: ").lower()
        
        if response == 'yes':
            print("Please submit the application manually.")
            input("Press Enter when done...")
        else:
            print("Application not submitted.")
    
    def _semi_auto_submit(self, page: Page) -> None:
        """Handle submission in semi-auto mode."""
        print("\n📋 Application filled. Ready to submit.")
        response = input("Press Enter to submit, or 'c' to cancel: ").lower()
        
        if response != 'c':
            self._find_and_click_submit(page)
    
    def _full_auto_submit(self, page: Page) -> None:
        """Handle submission in full-auto mode."""
        print("\n⚠️  About to submit application!")
        response = input("Type 'SUBMIT' to confirm: ")
        
        if response == 'SUBMIT':
            self._find_and_click_submit(page)
        else:
            print("Submission cancelled.")
    
    def _find_and_click_submit(self, page: Page) -> bool:
        """Find and click submit button.
        
        Args:
            page: Playwright page
            
        Returns:
            True if button was clicked
        """
        submit_patterns = [
            'button:has-text("Submit")',
            'button:has-text("Apply")',
            'button:has-text("Send")',
            'input[type="submit"]',
            'button[type="submit"]'
        ]
        
        for pattern in submit_patterns:
            try:
                button = page.query_selector(pattern)
                if button:
                    button.click()
                    print("✓ Application submitted!")
                    return True
            except Exception:
                continue
        
        print("⚠️  Could not find submit button. Please submit manually.")
        return False
