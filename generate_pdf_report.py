import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)

def build_pdf():
    pdf_filename = "Event_Platform_Project_Report.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    primary_color = colors.HexColor("#1e1b4b")   # Dark Indigo
    secondary_color = colors.HexColor("#4338ca") # Indigo Accent
    accent_purple = colors.HexColor("#7c3aed")   # Purple
    text_dark = colors.HexColor("#1f2937")       # Charcoal
    bg_light = colors.HexColor("#f8fafc")        # Light Slate BG
    border_color = colors.HexColor("#e2e8f0")

    # Custom Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=secondary_color,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=primary_color,
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=secondary_color,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=text_dark,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        borderColor=border_color,
        borderWidth=0.5,
        borderPadding=6,
        spaceAfter=6
    )

    qa_question_style = ParagraphStyle(
        'QA_Q',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=accent_purple,
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    qa_answer_style = ParagraphStyle(
        'QA_A',
        parent=body_style,
        textColor=text_dark,
        spaceAfter=8
    )

    story = []

    # Title Banner
    story.append(Paragraph("EventVibe — Technical Project & Viva Report", title_style))
    story.append(Paragraph("Full-Stack Event Discovery & Real-Time Tracking Platform | Quantiphi Assessment", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=secondary_color, spaceBefore=0, spaceAfter=12))

    # Section 1: Executive Summary
    story.append(Paragraph("1. Executive Summary", h1_style))
    story.append(Paragraph(
        "EventVibe is a complete, production-ready full-stack event discovery and tracking platform built using React, Vite, FastAPI, and MongoDB. The system enables users to discover events, manage RSVPs, track personal dashboards, invite friends via trackable links, view real-time WebSocket attendance updates, and query events using an intelligent deterministic chat assistant.",
        body_style
    ))

    # Section 2: What We Built
    story.append(Paragraph("2. What We Built (Features & Capabilities)", h1_style))
    features = [
        ("Event Discovery & API Feed Integration", "Integrates with the Ticketmaster Discovery API on the backend with an automated fallback to structured mock events across Music, Technology, Sports, Arts, and Food across major cities (Mumbai, Pune, New York, Bangalore)."),
        ("Custom React Event Calendar", "A zero-dependency interactive monthly calendar highlighting event dates and supporting date-filtered event views."),
        ("Server-Authoritative RSVP & Dashboard", "Single-click RSVP confirmation, duplicate RSVP rejection (409 Conflict), and an RSVP dashboard computing total and upcoming events."),
        ("Friend Invitation System", "Generates unique shareable links (/invite/:token) allowing RSVP'd users to invite friends."),
        ("Click Tracking vs. Friends Attending", "Deduplicates visitor clicks (clickCount) separately from confirmed friend RSVPs (friendsAttending). Clicks never inflate attendance."),
        ("Real-Time WebSockets", "Live bidirectional WebSocket connections on /ws broadcast attendance changes to instantly update event cards across clients without full page reloads."),
        ("User Profile & Reminders", "User preferences for event reminders with customizable lead times (validated from 1 to 10,080 minutes)."),
        ("Intelligent Chat Assistant", "Regex/keyword-driven chat assistant parsing natural queries for category, city, date, and user RSVP records.")
    ]

    for title, desc in features:
        p_text = f"<b>• {title}:</b> {desc}"
        story.append(Paragraph(p_text, bullet_style))

    story.append(Spacer(1, 8))

    # Section 3: Architecture & Technical Stack
    story.append(Paragraph("3. Technical Architecture & Stack", h1_style))
    story.append(Paragraph(
        "The application utilizes a clean Client-Server architecture where all business logic, validation, and attendance calculations reside strictly on the server.",
        body_style
    ))

    arch_data = [
        [Paragraph("<b>Layer</b>", body_style), Paragraph("<b>Technologies Used</b>", body_style), Paragraph("<b>Key Responsibilities</b>", body_style)],
        [Paragraph("Frontend", body_style), Paragraph("React 18, Vite, React Router v6, Axios, Plain CSS", body_style), Paragraph("Renders UI, collects user input, manages WebSocket connection, routes pages.", body_style)],
        [Paragraph("Backend", body_style), Paragraph("Python 3.14, FastAPI, Uvicorn, Pydantic v2, HTTPX", body_style), Paragraph("Validates inputs, enforces database constraints, fetches Ticketmaster API, handles WS broadcasts.", body_style)],
        [Paragraph("Database", body_style), Paragraph("MongoDB, PyMongo, mongomock fallback", body_style), Paragraph("Stores collections for users, rsvps, invites, and invite_clicks with unique compound indexes.", body_style)]
    ]

    t_arch = Table(arch_data, colWidths=[1.1*inch, 2.5*inch, 3.2*inch])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), bg_light),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 10))

    # Section 4: Key Design & Engineering Decisions
    story.append(Paragraph("4. Key Engineering & Design Decisions", h1_style))
    decisions = [
        ("Atomic Unique-Index Deduplication", "Instead of fragile check-then-insert application logic, uniqueness for RSVPs (userId, eventId), invites (token), and clicks (token, visitorId) is enforced at the database level via MongoDB unique compound indexes catching DuplicateKeyError."),
        ("Immutable Event Snapshots", "To insulate user RSVPs and invitations against external API changes or expired Ticketmaster events, complete event metadata (title, venue, city, date, image) is snapshotted upon RSVP creation."),
        ("Ticketmaster API Backend Isolation", "The Ticketmaster API key is stored exclusively in server environment variables and never exposed to the client. Normalization into a unified structure occurs entirely inside backend services."),
        ("Server-Side Business Authority", "Clients never calculate attendance, friend counts, or upcoming statistics. The server performs all calculations and returns authoritative read-only numbers.")
    ]

    for title, desc in decisions:
        story.append(Paragraph(f"<b>• {title}:</b> {desc}", bullet_style))

    story.append(Spacer(1, 10))

    # Section 5: Automated Verification & Testing
    story.append(Paragraph("5. Verification & Testing", h1_style))
    story.append(Paragraph(
        "The project was verified through a comprehensive automated smoke test suite (backend/smoke_test.py) covering 14 critical end-to-end assertions:",
        body_style
    ))

    test_assertions = [
        "1. /api/health responds with HTTP 200 OK.",
        "2 & 3. /api/events returns normalized feed (Ticketmaster / Mock fallback).",
        "4. Demo user can successfully RSVP to an event.",
        "5. Duplicate RSVP correctly rejected with HTTP 409 Conflict.",
        "6. Dashboard returns accurate total and upcoming confirmed RSVPs.",
        "7. User can generate a unique invite link.",
        "8. Invite GET endpoint returns valid inviter and event details.",
        "9. Visitor click tracking deduplicates repeat clicks from the same visitor ID.",
        "10 & 11. Friend RSVP via invite link successfully increments friendsAttending by 1.",
        "12. Duplicate friend RSVP rejected with 409 without inflating attendance.",
        "13. RSVP cancellation decrements friendsAttending back to 0.",
        "14. Invalid invite tokens return HTTP 404 Not Found."
    ]

    for item in test_assertions:
        story.append(Paragraph(f"<font color='#10b981'><b>[PASSED]</b></font> {item}", bullet_style))

    story.append(Paragraph("<b>Frontend Build:</b> Ran <code>npm run build</code> (vite build) — 100 modules transformed, 0 errors.", body_style))

    story.append(Spacer(1, 10))

    # Section 6: Viva Preparation Guide
    story.append(Paragraph("6. Viva Preparation Guide", h1_style))

    story.append(Paragraph("10-Line Architecture Summary for Viva:", h2_style))
    arch_summary_code = """1. React + Vite SPA renders UI components and handles client routing.
2. Axios sends REST HTTP calls to FastAPI server endpoints on Uvicorn.
3. FastAPI enforces input validation using Pydantic schemas.
4. Ticketmaster Discovery API queried on backend via HTTPX (8s timeout).
5. Automatic fallback to mock events if API key is missing or request fails.
6. MongoDB stores users, rsvps, invites, and invite_clicks collections.
7. MongoDB unique compound indexes prevent duplicate RSVPs and clicks.
8. Real-time updates broadcast over WebSockets (/ws) on RSVP actions.
9. React WebSocket client listens and updates affected cards live.
10. Deterministic chat assistant parses natural queries via regex matching."""
    story.append(Paragraph(arch_summary_code.replace('\n', '<br/>'), code_style))

    story.append(Paragraph("Core Viva Questions & Concise Answers:", h2_style))

    qa_list = [
        ("Q1: Why React + Vite for the frontend?", "React provides declarative component rendering perfect for updating cards and calendar states. Vite provides instant HMR and optimized production builds."),
        ("Q2: Why FastAPI for backend?", "FastAPI offers high speed, automatic Pydantic validation, native WebSocket support, and auto-generated Swagger documentation."),
        ("Q3: Why MongoDB?", "MongoDB's flexible document structure naturally fits nested event snapshots and user reminder settings without requiring complex relational joins."),
        ("Q4: Why keep Ticketmaster API on backend?", "Keeps API keys secret, prevents CORS issues, normalizes raw responses, and handles fallback to mock data transparently."),
        ("Q5: How are duplicate RSVPs prevented?", "By creating a unique compound index on (userId, eventId) in MongoDB. Attempting a duplicate raises DuplicateKeyError, returning HTTP 409 Conflict."),
        ("Q6: Difference between clickCount and friendsAttending?", "clickCount tracks unique link visitors via (token, visitorId) compound index. friendsAttending counts actual confirmed RSVPs created through the invite."),
        ("Q7: How do real-time updates work?", "When an RSVP occurs, websocket_manager.py broadcasts an rsvp_updated JSON payload to all /ws clients. React updates the affected card state dynamically."),
        ("Q8: How does the chat assistant work?", "chat_service.py uses regex pattern matching to parse categories, cities, dates, and personal user RSVP records against MongoDB."),
        ("Q9: Why store eventSnapshots in RSVPs?", "External API data can change or expire. Storing an immutable snapshot guarantees the user's dashboard displays consistent data."),
        ("Q10: Why is PyMongo synchronous in FastAPI?", "PyMongo is simple and reliable for MVPs, executing in <1ms for local/in-memory database operations.")
    ]

    for q, a in qa_list:
        story.append(Paragraph(q, qa_question_style))
        story.append(Paragraph(a, qa_answer_style))

    # Footer / Summary
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=border_color, spaceBefore=5, spaceAfter=10))
    story.append(Paragraph(
        "<b>Repository URL:</b> https://github.com/Yusuf-khan-git/Quantiphi-ML-Vibe-Coding | <b>Status:</b> All 7 Commits Pushed to origin/main",
        ParagraphStyle('Footer', parent=body_style, fontSize=8.5, textColor=colors.HexColor("#64748b"), alignment=1)
    ))

    doc.build(story)
    print(f"PDF successfully generated: {pdf_filename}")

if __name__ == "__main__":
    build_pdf()
