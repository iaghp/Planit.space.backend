"""Main CLI application using Typer."""

from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

from src.config_manager import ConfigManager
from src.cover_letter import CoverLetterGenerator, load_job_description
from src.pdf_formatter import PDFFormatter, generate_filename
from src.resume_tailor import ResumeTailor
from src.auto_apply import AutoApply, AutoFillMode

app = typer.Typer(
    name="job-apply",
    help="CLI-based Job Application Automation Suite",
    add_completion=False
)
console = Console()


@app.command()
def cover_letter(
    job_desc: Optional[str] = typer.Option(None, "--job-desc", help="Job description text"),
    job_desc_file: Optional[Path] = typer.Option(None, "--job-desc-file", help="Job description file path"),
    company: str = typer.Option(..., "--company", help="Company name"),
    role: str = typer.Option(..., "--role", help="Job role/title"),
    notes: Optional[str] = typer.Option(None, "--notes", help="Custom instructions for AI"),
    hiring_manager: Optional[str] = typer.Option(None, "--hiring-manager", help="Hiring manager name"),
    ai_provider: str = typer.Option("openai", "--ai-provider", help="AI provider (openai or anthropic)"),
    output: Optional[Path] = typer.Option(None, "--output", help="Output PDF path")
) -> None:
    """Generate a personalized cover letter."""
    try:
        console.print(Panel.fit("🚀 Cover Letter Generator", style="bold blue"))
        
        # Load job description
        if job_desc_file:
            job_description = load_job_description(str(job_desc_file))
        elif job_desc:
            job_description = job_desc
        else:
            console.print("Please paste the job description (Ctrl+D when done):")
            job_description = typer.get_text_stream("stdin").read()
        
        # Generate cover letter
        console.print(f"\n✨ Generating cover letter for [bold]{role}[/bold] at [bold]{company}[/bold]...")
        
        config = ConfigManager()
        generator = CoverLetterGenerator(config, ai_provider)
        
        content = generator.generate_full_letter(
            job_description,
            company,
            role,
            notes,
            hiring_manager
        )
        
        # Generate PDF
        if not output:
            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)
            filename = generate_filename(company, "CoverLetter")
            output = output_dir / filename
        
        formatter = PDFFormatter(config)
        pdf_path = formatter.create_cover_letter_pdf(content, output, company)
        
        console.print(f"\n✅ Cover letter saved to: [green]{pdf_path}[/green]")
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def tailor_resume(
    job_desc: Optional[str] = typer.Option(None, "--job-desc", help="Job description text"),
    job_desc_file: Optional[Path] = typer.Option(None, "--job-desc-file", help="Job description file path"),
    resume: Path = typer.Option(..., "--resume", help="Path to base resume"),
    notes: Optional[str] = typer.Option(None, "--notes", help="Custom instructions"),
    ai_provider: str = typer.Option("openai", "--ai-provider", help="AI provider"),
    output: Optional[Path] = typer.Option(None, "--output", help="Output PDF path")
) -> None:
    """Tailor your resume to a job description."""
    try:
        console.print(Panel.fit("📄 Resume Tailor", style="bold blue"))
        
        # Load job description
        if job_desc_file:
            job_description = load_job_description(str(job_desc_file))
        elif job_desc:
            job_description = job_desc
        else:
            console.print("Please paste the job description (Ctrl+D when done):")
            job_description = typer.get_text_stream("stdin").read()
        
        # Tailor resume
        console.print("\n✨ Tailoring resume...")
        
        config = ConfigManager()
        tailor = ResumeTailor(config, ai_provider)
        
        tailored_content = tailor.tailor_resume(resume, job_description, notes)
        
        # Save to file
        if not output:
            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)
            output = output_dir / "resume_tailored.txt"
        
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(tailored_content, encoding='utf-8')
        
        console.print(f"\n✅ Tailored resume saved to: [green]{output}[/green]")
        console.print("\n💡 Tip: Review and convert to PDF using your preferred tool.")
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def auto_fill(
    url: str = typer.Option(..., "--url", help="Job application URL"),
    mode: str = typer.Option("supervised", "--mode", help="Mode: supervised, semi-auto, full-auto"),
    resume: Optional[Path] = typer.Option(None, "--resume", help="Resume PDF path"),
    cover_letter: Optional[Path] = typer.Option(None, "--cover-letter", help="Cover letter PDF path"),
    headless: bool = typer.Option(False, "--headless", help="Run browser in headless mode")
) -> None:
    """Auto-fill a job application form."""
    try:
        console.print(Panel.fit("🌐 Auto-Fill Application", style="bold blue"))
        
        # Parse mode
        try:
            fill_mode = AutoFillMode(mode.lower())
        except ValueError:
            console.print(f"[red]Invalid mode:[/red] {mode}. Use: supervised, semi-auto, or full-auto")
            raise typer.Exit(1)
        
        # Run auto-fill
        console.print(f"\n🤖 Starting auto-fill in [bold]{mode}[/bold] mode...")
        
        config = ConfigManager()
        bot = AutoApply(config, fill_mode, headless)
        
        success = bot.fill_application(url, resume, cover_letter)
        
        if success:
            console.print("\n✅ Auto-fill completed!")
        else:
            console.print("\n⚠️  Auto-fill encountered errors.")
            raise typer.Exit(1)
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def apply() -> None:
    """Full pipeline: generate cover letter, tailor resume, and auto-fill application."""
    try:
        console.print(Panel.fit("🎯 Complete Application Pipeline", style="bold bold blue"))
        
        # Gather information
        console.print("\n[bold]Step 1: Job Information[/bold]")
        company = Prompt.ask("Company name")
        role = Prompt.ask("Job role/title")
        url = Prompt.ask("Application URL (optional)", default="")
        
        console.print("\n[bold]Paste job description[/bold] (press Ctrl+D when done):")
        job_description = typer.get_text_stream("stdin").read()
        
        # Ask for customization
        notes = Prompt.ask("Any custom instructions? (optional)", default="")
        
        # Step 2: Generate cover letter
        console.print("\n[bold]Step 2: Generating Cover Letter[/bold]")
        
        config = ConfigManager()
        generator = CoverLetterGenerator(config)
        
        cover_letter_content = generator.generate_full_letter(
            job_description,
            company,
            role,
            notes if notes else None
        )
        
        # Save cover letter
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        cover_letter_path = output_dir / generate_filename(company, "CoverLetter")
        formatter = PDFFormatter(config)
        formatter.create_cover_letter_pdf(cover_letter_content, cover_letter_path, company)
        
        console.print(f"✅ Cover letter: [green]{cover_letter_path}[/green]")
        
        # Step 3: Tailor resume (optional)
        if Confirm.ask("\nTailor your resume?"):
            console.print("\n[bold]Step 3: Tailoring Resume[/bold]")
            
            base_resume = Prompt.ask("Path to base resume")
            base_resume_path = Path(base_resume)
            
            if base_resume_path.exists():
                tailor = ResumeTailor(config)
                tailored_content = tailor.tailor_resume(
                    base_resume_path,
                    job_description,
                    notes if notes else None
                )
                
                resume_path = output_dir / "resume_tailored.txt"
                resume_path.write_text(tailored_content, encoding='utf-8')
                
                console.print(f"✅ Tailored resume: [green]{resume_path}[/green]")
            else:
                console.print("[yellow]Resume file not found, skipping...[/yellow]")
                resume_path = None
        else:
            resume_path = None
        
        # Step 4: Auto-fill (optional)
        if url and Confirm.ask("\nAuto-fill the application?"):
            console.print("\n[bold]Step 4: Auto-Filling Application[/bold]")
            
            bot = AutoApply(config, AutoFillMode.SUPERVISED)
            bot.fill_application(url, resume_path, cover_letter_path)
        
        console.print("\n✨ [bold green]Application process complete![/bold green]")
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def config() -> None:
    """Interactively configure your profile."""
    try:
        console.print(Panel.fit("⚙️  Configuration Setup", style="bold blue"))
        
        config_manager = ConfigManager()
        config_dir = config_manager.config_dir
        
        # Check if profile exists
        profile_path = config_dir / "profile.yaml"
        example_path = config_dir / "profile.yaml.example"
        
        if profile_path.exists():
            if not Confirm.ask(f"Profile already exists at {profile_path}. Overwrite?"):
                console.print("Configuration cancelled.")
                return
        
        # Copy example to profile
        if example_path.exists():
            import shutil
            shutil.copy(example_path, profile_path)
            console.print(f"\n✅ Created profile template at: [green]{profile_path}[/green]")
            console.print("\n📝 Please edit this file with your information:")
            console.print(f"   {profile_path}")
        else:
            console.print(f"[yellow]Example profile not found at {example_path}[/yellow]")
        
        # Check for .env
        env_path = config_dir.parent / ".env"
        if not env_path.exists():
            console.print("\n⚠️  No .env file found. Create one with your API keys:")
            console.print("   OPENAI_API_KEY=sk-...")
            console.print("   ANTHROPIC_API_KEY=sk-ant-...")
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def version() -> None:
    """Show version information."""
    from src import __version__
    console.print(f"job-apply version {__version__}")


if __name__ == "__main__":
    app()
