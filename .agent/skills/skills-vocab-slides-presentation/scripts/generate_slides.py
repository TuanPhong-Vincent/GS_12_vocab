#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classroom Slide Deck & Presentation Generator Script (All-English Classroom Immersion Edition)
Features:
- 100% English UI and slide content
- Fully responsive slide viewport with auto-scroll and zero content truncation
- Teacher-controlled progressive answer reveals for thinking time across all exercises
- Interactive CCQ reveal buttons
- Dual-mode Projector View & Teacher Presenter View with live teleprompter
"""

import os
import sys
import json
import argparse
from pathlib import Path

SLIDES_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{deck_title} - Interactive Classroom Presentation Deck</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Be+Vietnam+Pro:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-canvas: #090d16;
            --bg-slide: #0f172a;
            --bg-card: #1e293b;
            --bg-card-subtle: #162032;
            --border: #334155;
            --border-highlight: #3b82f6;
            --primary: #2563eb;
            --primary-glow: rgba(37, 99, 235, 0.35);
            --accent: #38bdf8;
            --accent-glow: rgba(56, 189, 248, 0.3);
            --success: #10b981;
            --success-glow: rgba(16, 185, 129, 0.35);
            --warning: #f59e0b;
            --danger: #ef4444;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --text-dim: #64748b;
            --font-display: 'Plus Jakarta Sans', sans-serif;
            --font-body: 'Be Vietnam Pro', sans-serif;
            --radius-lg: 16px;
            --radius-md: 10px;
            --radius-sm: 6px;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            background-color: var(--bg-canvas);
            color: var(--text-main);
            font-family: var(--font-body);
            overflow: hidden;
            height: 100vh;
            width: 100vw;
            display: flex;
            flex-direction: column;
            user-select: none;
        }}

        /* TOP NAVIGATION & CONTROLS */
        .top-bar {{
            height: 50px;
            background: rgba(15, 23, 42, 0.9);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 20px;
            z-index: 50;
            flex-shrink: 0;
        }}

        .brand-area {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .unit-badge {{
            background: linear-gradient(135deg, #1e40af, #2563eb);
            color: #ffffff;
            font-family: var(--font-display);
            font-weight: 800;
            font-size: 12px;
            padding: 4px 10px;
            border-radius: 9999px;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }}

        .slide-title-header {{
            font-family: var(--font-display);
            font-size: 14px;
            font-weight: 700;
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .stage-pill {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            color: var(--accent);
            font-size: 11.5px;
            font-weight: 600;
            padding: 2px 8px;
            border-radius: 4px;
        }}

        .controls-area {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .ctrl-btn {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            color: var(--text-main);
            font-family: var(--font-display);
            font-size: 12px;
            font-weight: 600;
            padding: 5px 11px;
            border-radius: var(--radius-sm);
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s ease;
        }}

        .ctrl-btn:hover {{
            background: #2563eb;
            border-color: #3b82f6;
            color: #ffffff;
            box-shadow: 0 0 12px var(--primary-glow);
        }}

        .ctrl-btn.active {{
            background: #2563eb;
            border-color: #60a5fa;
            color: #ffffff;
        }}

        .step-progress-indicator {{
            display: flex;
            align-items: center;
            gap: 5px;
            margin-right: 6px;
        }}

        .step-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--border);
            transition: all 0.3s ease;
        }}

        .step-dot.active {{
            background: var(--accent);
            transform: scale(1.3);
            box-shadow: 0 0 8px var(--accent);
        }}

        .step-dot.done {{
            background: var(--success);
        }}

        /* PRESENTATION MAIN VIEWPORT */
        .presentation-viewport {{
            flex: 1;
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 14px 20px;
        }}

        /* SLIDE CONTAINER - RESPONSIVE & NO OVERFLOW CUTOFF */
        .slide-canvas {{
            width: 100%;
            max-width: 1440px;
            height: calc(100vh - 108px);
            max-height: 860px;
            background: var(--bg-slide);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.7);
            position: relative;
            display: none;
            flex-direction: column;
            padding: 22px 32px;
            overflow-y: auto;
            overflow-x: hidden;
        }}

        .slide-canvas.active-slide {{
            display: flex;
            animation: slideFadeIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }}

        @keyframes slideFadeIn {{
            from {{
                opacity: 0;
                transform: scale(0.99);
            }}
            to {{
                opacity: 1;
                transform: scale(1);
            }}
        }}

        /* CUSTOM MODERN SCROLLBAR */
        .slide-canvas::-webkit-scrollbar,
        .lexis-col::-webkit-scrollbar,
        .ccq-container::-webkit-scrollbar,
        .presenter-drawer::-webkit-scrollbar {{
            width: 6px;
        }}
        .slide-canvas::-webkit-scrollbar-track,
        .lexis-col::-webkit-scrollbar-track,
        .ccq-container::-webkit-scrollbar-track,
        .presenter-drawer::-webkit-scrollbar-track {{
            background: rgba(15, 23, 42, 0.5);
            border-radius: 4px;
        }}
        .slide-canvas::-webkit-scrollbar-thumb,
        .lexis-col::-webkit-scrollbar-thumb,
        .ccq-container::-webkit-scrollbar-thumb,
        .presenter-drawer::-webkit-scrollbar-thumb {{
            background: #334155;
            border-radius: 4px;
        }}
        .slide-canvas::-webkit-scrollbar-thumb:hover {{
            background: #3b82f6;
        }}

        /* SLIDE TOP HEADER */
        .slide-top-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            flex-shrink: 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding-bottom: 12px;
        }}

        .slide-title-wrap h2 {{
            font-family: var(--font-display);
            font-size: 22px;
            font-weight: 800;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 10px;
            letter-spacing: -0.5px;
        }}

        .slide-subtitle {{
            font-size: 13px;
            color: var(--text-muted);
            margin-top: 2px;
            font-weight: 500;
        }}

        .slide-meta-pills {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .time-badge {{
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid var(--border);
            color: #facc15;
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 12px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 5px;
        }}

        .involvement-badge {{
            background: rgba(14, 165, 233, 0.15);
            border: 1px solid rgba(14, 165, 233, 0.3);
            color: #38bdf8;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 11.5px;
            font-weight: 700;
        }}

        /* SLIDE BODY LAYOUT */
        .slide-body-grid {{
            flex: 1;
            display: grid;
            grid-template-columns: 1.15fr 1.35fr;
            gap: 28px;
            overflow: hidden;
            position: relative;
        }}

        .slide-body-grid.single-col {{
            grid-template-columns: 1fr;
            overflow-y: visible;
        }}

        /* LEFT COLUMN: VISUAL CONTEXT & CCQs */
        .visual-col {{
            display: flex;
            flex-direction: column;
            gap: 14px;
            height: 100%;
            overflow: hidden;
        }}

        .image-frame {{
            background: #000000;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid var(--border);
            position: relative;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
            max-height: 230px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }}

        .image-frame img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
            transition: transform 0.4s ease;
        }}

        .image-caption-box {{
            background: rgba(15, 23, 42, 0.9);
            border-left: 3px solid var(--accent);
            padding: 8px 12px;
            border-radius: 0 8px 8px 0;
            font-size: 12.5px;
            color: #cbd5e1;
            line-height: 1.45;
            display: flex;
            align-items: flex-start;
            gap: 8px;
        }}

        .image-caption-box strong {{
            color: #38bdf8;
            white-space: nowrap;
        }}

        /* CCQ CARDS CONTAINER */
        .ccq-container {{
            display: flex;
            flex-direction: column;
            gap: 8px;
            flex: 1;
            overflow-y: auto;
            padding-right: 4px;
        }}

        .ccq-title-badge {{
            font-family: var(--font-display);
            font-size: 12px;
            font-weight: 700;
            color: #38bdf8;
            display: flex;
            align-items: center;
            justify-content: space-between;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 2px;
        }}

        .ccq-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 10px 14px;
            transition: all 0.25s ease;
            opacity: 0.35;
            cursor: pointer;
        }}

        .ccq-card.revealed {{
            opacity: 1;
            border-color: #3b82f6;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        }}

        .ccq-q {{
            font-size: 13.5px;
            font-weight: 600;
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
            line-height: 1.4;
        }}

        .ccq-q-left {{
            display: flex;
            align-items: flex-start;
            gap: 8px;
        }}

        .ccq-q-num {{
            background: #2563eb;
            color: #ffffff;
            font-size: 11px;
            font-weight: 800;
            padding: 2px 6px;
            border-radius: 4px;
            flex-shrink: 0;
            margin-top: 1px;
        }}

        .reveal-hint-btn {{
            background: rgba(37, 99, 235, 0.2);
            border: 1px solid rgba(59, 130, 246, 0.4);
            color: #93c5fd;
            font-size: 11px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 4px;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.2s ease;
        }}

        .reveal-hint-btn:hover {{
            background: #2563eb;
            color: #ffffff;
        }}

        .ccq-a {{
            margin-top: 8px;
            padding: 7px 12px;
            background: rgba(16, 185, 129, 0.15);
            border: 1px solid rgba(16, 185, 129, 0.35);
            border-radius: 6px;
            color: #6ee7b7;
            font-size: 13px;
            font-weight: 600;
            display: none;
            align-items: center;
            gap: 8px;
            animation: fadeIn 0.2s ease forwards;
        }}

        .ccq-a.show-answer {{
            display: flex;
        }}

        /* RIGHT COLUMN: SPOKEN, WRITTEN FORM, COLLOCATION GRID */
        .lexis-col {{
            display: flex;
            flex-direction: column;
            gap: 14px;
            height: 100%;
            overflow-y: auto;
            padding-right: 4px;
        }}

        /* PHONETICS & AUDIO CARD (STEP 3) */
        .phonetics-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 12px 18px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            opacity: 0.2;
            transition: all 0.3s ease;
        }}

        .phonetics-card.revealed {{
            opacity: 1;
            border-color: #38bdf8;
            box-shadow: 0 0 16px var(--accent-glow);
        }}

        .ipa-wrap {{
            display: flex;
            flex-direction: column;
            gap: 3px;
        }}

        .ipa-text {{
            font-family: var(--font-display);
            font-size: 22px;
            font-weight: 700;
            color: #38bdf8;
            letter-spacing: 0.5px;
        }}

        .stress-beat {{
            font-size: 13px;
            color: #cbd5e1;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .stress-beat span.primary {{
            color: #facc15;
            font-weight: 800;
            text-transform: uppercase;
        }}

        .audio-actions {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .play-audio-btn {{
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            border: 2px solid #60a5fa;
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
        }}

        .play-audio-btn:hover {{
            transform: scale(1.08);
            box-shadow: 0 0 18px rgba(96, 165, 250, 0.8);
        }}

        .mumble-drill-badge {{
            background: rgba(245, 158, 11, 0.15);
            border: 1px solid rgba(245, 158, 11, 0.3);
            color: #fbbf24;
            padding: 7px 12px;
            border-radius: 8px;
            font-size: 12.5px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 6px;
            cursor: pointer;
        }}

        .mumble-drill-badge:hover {{
            background: rgba(245, 158, 11, 0.25);
        }}

        /* WRITTEN FORM & SPELLING TRAP CARD (STEP 4) */
        .written-form-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 16px 20px;
            opacity: 0.2;
            transition: all 0.3s ease;
        }}

        .written-form-card.revealed {{
            opacity: 1;
            border-color: #60a5fa;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.35);
        }}

        .headword-banner {{
            display: flex;
            align-items: baseline;
            gap: 12px;
            margin-bottom: 10px;
            flex-wrap: wrap;
        }}

        .headword {{
            font-family: var(--font-display);
            font-size: 28px;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: -0.5px;
        }}

        .headword span.trap-highlight {{
            color: #ef4444;
            text-decoration: underline;
            text-decoration-thickness: 3px;
            text-underline-offset: 4px;
            font-weight: 900;
        }}

        .definition-en {{
            font-size: 14.5px;
            color: #94a3b8;
            font-weight: 500;
        }}

        .spelling-trap-alert {{
            background: rgba(239, 68, 68, 0.12);
            border: 1px dashed rgba(239, 68, 68, 0.4);
            border-radius: 8px;
            padding: 8px 12px;
            color: #fca5a5;
            font-size: 12.5px;
            line-height: 1.45;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .spelling-trap-alert strong {{
            color: #ffffff;
            background: #b91c1c;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 11px;
            text-transform: uppercase;
        }}

        /* COLLOCATION GRID & SENTENCE FRAME (STEP 5) */
        .collocation-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 16px 20px;
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 12px;
            opacity: 0.2;
            transition: all 0.3s ease;
        }}

        .collocation-card.revealed {{
            opacity: 1;
            border-color: #10b981;
            box-shadow: 0 0 16px var(--success-glow);
        }}

        .collocation-grid-display {{
            background: #0f172a;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 10px 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 14px;
            flex-wrap: wrap;
        }}

        .colloc-left-branch {{
            display: flex;
            flex-direction: column;
            gap: 4px;
            text-align: right;
        }}

        .colloc-item {{
            background: rgba(56, 189, 248, 0.15);
            color: #38bdf8;
            border: 1px solid rgba(56, 189, 248, 0.3);
            font-family: var(--font-display);
            font-size: 13px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 6px;
        }}

        .colloc-center-word {{
            font-family: var(--font-display);
            font-size: 18px;
            font-weight: 800;
            color: #facc15;
            padding: 6px 14px;
            background: #1e293b;
            border: 2px solid #facc15;
            border-radius: 8px;
            text-transform: uppercase;
            box-shadow: 0 0 12px rgba(250, 204, 21, 0.25);
        }}

        .sentence-frame-box {{
            background: rgba(30, 41, 59, 0.7);
            border-left: 4px solid #10b981;
            border-radius: 0 8px 8px 0;
            padding: 10px 14px;
        }}

        .sentence-frame-box h5 {{
            color: #6ee7b7;
            font-size: 11.5px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        }}

        .frame-text {{
            font-size: 14px;
            color: #ffffff;
            font-style: italic;
            line-height: 1.45;
        }}

        .frame-text span.fill-spot {{
            color: #facc15;
            font-weight: 700;
            text-decoration: underline;
        }}

        /* TIMERS & ACTIONS */
        .timer-widget {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 6px 12px;
            margin-top: auto;
        }}

        .timer-display {{
            font-family: var(--font-display);
            font-size: 17px;
            font-weight: 800;
            color: #facc15;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .timer-btn-group {{
            display: flex;
            gap: 6px;
        }}

        .timer-btn {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            color: var(--text-main);
            font-size: 11px;
            font-weight: 700;
            padding: 4px 9px;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .timer-btn:hover {{
            background: #2563eb;
            color: #ffffff;
        }}

        /* PRACTICE & ODD-ONE-OUT BLITZ STYLES (COMPACT & PREVENT CUTOFF) */
        .practice-question-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 10px 16px;
            margin-bottom: 8px;
            transition: all 0.2s ease;
        }}

        .practice-q-text {{
            font-size: 14.5px;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 8px;
            line-height: 1.4;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .practice-q-text span.clue-target {{
            padding: 2px 6px;
            border-radius: 4px;
            transition: all 0.3s ease;
        }}

        .practice-q-text span.clue-target.highlight-clue {{
            background: rgba(245, 158, 11, 0.25);
            border-bottom: 2px solid #facc15;
            color: #facc15;
            font-weight: 700;
        }}

        .practice-options-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 6px;
        }}

        .practice-opt {{
            background: var(--bg-card-subtle);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 7px 12px;
            font-size: 13.5px;
            color: #cbd5e1;
            display: flex;
            align-items: center;
            justify-content: space-between;
            transition: all 0.25s ease;
        }}

        .practice-opt.impostor-target.revealed {{
            background: rgba(239, 68, 68, 0.2);
            border-color: #ef4444;
            color: #fca5a5;
        }}

        .impostor-badge {{
            display: none;
            background: #b91c1c;
            color: #ffffff;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 700;
            animation: fadeIn 0.25s ease forwards;
        }}

        .practice-opt.impostor-target.revealed .impostor-badge {{
            display: inline-flex;
            align-items: center;
        }}

        .practice-opt.is-correct.correct-answer {{
            background: rgba(16, 185, 129, 0.2);
            border-color: #10b981;
            color: #6ee7b7;
            font-weight: 700;
        }}

        .reveal-action-btn {{
            background: rgba(59, 130, 246, 0.2);
            border: 1px solid #3b82f6;
            color: #93c5fd;
            font-size: 11.5px;
            font-weight: 700;
            padding: 3px 9px;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .reveal-action-btn:hover {{
            background: #2563eb;
            color: #ffffff;
        }}

        /* WORD FAMILY TABLE MASKING */
        .masked-cell {{
            background: rgba(30, 41, 59, 0.8);
            border: 1px dashed #475569;
            color: #94a3b8;
            padding: 3px 8px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12.5px;
            display: inline-block;
            transition: all 0.2s ease;
        }}

        .masked-cell.revealed {{
            background: rgba(16, 185, 129, 0.2);
            border: 1px solid #10b981;
            color: #6ee7b7;
            font-weight: 700;
        }}

        /* TEACHER PRESENTER TELEPROMPTER DRAWER */
        .presenter-drawer {{
            position: fixed;
            top: 50px;
            right: 0;
            width: 440px;
            height: calc(100vh - 50px);
            background: #0b1120;
            border-left: 2px solid #2563eb;
            box-shadow: -15px 0 40px rgba(0, 0, 0, 0.7);
            z-index: 100;
            display: flex;
            flex-direction: column;
            transform: translateX(100%);
            transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            padding: 22px;
            overflow-y: auto;
        }}

        .presenter-drawer.open {{
            transform: translateX(0);
        }}

        .drawer-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 18px;
            border-bottom: 1px solid var(--border);
            padding-bottom: 12px;
        }}

        .drawer-header h3 {{
            font-family: var(--font-display);
            font-size: 16px;
            font-weight: 800;
            color: #38bdf8;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .close-drawer-btn {{
            background: transparent;
            border: none;
            color: var(--text-muted);
            font-size: 20px;
            cursor: pointer;
        }}

        .prompter-section {{
            margin-bottom: 16px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 14px;
        }}

        .prompter-label {{
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            color: #facc15;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .teacher-talk-text {{
            font-size: 13.5px;
            line-height: 1.55;
            color: #ffffff;
            font-style: italic;
        }}

        .teacher-talk-vi {{
            font-size: 12.5px;
            line-height: 1.45;
            color: #94a3b8;
            margin-top: 6px;
            border-top: 1px dashed #334155;
            padding-top: 6px;
        }}

        .gesture-box {{
            background: rgba(14, 165, 233, 0.1);
            border: 1px solid rgba(14, 165, 233, 0.3);
            border-radius: 6px;
            padding: 9px;
            font-size: 12.5px;
            color: #7dd3fc;
            line-height: 1.45;
        }}

        .student-action-box {{
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 6px;
            padding: 9px;
            font-size: 12.5px;
            color: #a7f3d0;
            line-height: 1.45;
        }}

        .board-sync-box {{
            background: #020617;
            border: 1px solid #475569;
            border-radius: 6px;
            padding: 10px;
            font-size: 12px;
            line-height: 1.5;
            color: #cbd5e1;
        }}

        /* OVERVIEW GRID MODAL */
        .overview-modal {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(2, 6, 23, 0.92);
            backdrop-filter: blur(15px);
            z-index: 200;
            display: none;
            padding: 40px;
            overflow-y: auto;
        }}

        .overview-modal.open {{
            display: block;
        }}

        .overview-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
            gap: 16px;
            max-width: 1400px;
            margin: 0 auto;
        }}

        .overview-card {{
            background: var(--bg-card);
            border: 2px solid var(--border);
            border-radius: 10px;
            padding: 14px;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .overview-card:hover {{
            border-color: #3b82f6;
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(37, 99, 235, 0.3);
        }}

        .overview-card.current-slide {{
            border-color: #facc15;
            box-shadow: 0 0 16px rgba(250, 204, 21, 0.4);
        }}

        .ov-num {{
            font-size: 11.5px;
            font-weight: 800;
            color: #38bdf8;
            margin-bottom: 4px;
        }}

        .ov-title {{
            font-family: var(--font-display);
            font-size: 14px;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 6px;
        }}

        .ov-stage {{
            font-size: 11px;
            color: var(--text-muted);
        }}

        /* BLACKOUT SCREEN */
        .blackout-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: #000000;
            z-index: 300;
            display: none;
        }}

        .blackout-overlay.active {{
            display: block;
        }}

        /* CASCADE DIALOGUE SCENARIO */
        .cascade-flow {{
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-top: 8px;
        }}

        .turn-bubble {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 12px 18px;
            display: flex;
            align-items: flex-start;
            gap: 14px;
        }}

        .turn-bubble.partner-a {{
            border-left: 4px solid #38bdf8;
        }}

        .turn-bubble.partner-b {{
            border-left: 4px solid #facc15;
            margin-left: 36px;
        }}

        .speaker-badge {{
            font-family: var(--font-display);
            font-size: 12px;
            font-weight: 800;
            padding: 3px 8px;
            border-radius: 4px;
            flex-shrink: 0;
        }}

        .speaker-badge.a {{
            background: #0284c7;
            color: #ffffff;
        }}

        .speaker-badge.b {{
            background: #d97706;
            color: #ffffff;
        }}

        .dialogue-content {{
            font-size: 14.5px;
            color: #ffffff;
            line-height: 1.45;
        }}

        .dialogue-content strong.chunk-highlight {{
            color: #38bdf8;
            text-decoration: underline;
        }}

        /* MISSION CARD 1-MIN PITCH */
        .mission-hero-card {{
            background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 50%, #0f172a 100%);
            border: 2px solid #3b82f6;
            border-radius: 14px;
            padding: 24px;
            box-shadow: 0 12px 35px rgba(37, 99, 235, 0.25);
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}

        .mission-title {{
            font-family: var(--font-display);
            font-size: 22px;
            font-weight: 800;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .mission-criteria-list {{
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}

        .mission-criteria-list li {{
            font-size: 14px;
            color: #e2e8f0;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .mission-criteria-list li span.badge {{
            background: rgba(250, 204, 21, 0.2);
            color: #facc15;
            border: 1px solid rgba(250, 204, 21, 0.4);
            font-weight: 700;
            font-size: 11px;
            padding: 2px 7px;
            border-radius: 4px;
        }}

        /* EXIT TICKET SPECIFIC */
        .exit-ticket-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin-top: 12px;
        }}

        .exit-box {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}

        .exit-box h4 {{
            font-family: var(--font-display);
            font-size: 16px;
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .exit-box.b1 h4 {{ color: #38bdf8; }}
        .exit-box.b2 h4 {{ color: #10b981; }}
        .exit-box.b3 h4 {{ color: #ef4444; }}

        .exit-box p {{
            font-size: 13px;
            color: #cbd5e1;
            line-height: 1.45;
        }}

        /* BOTTOM FOOTER CONTROL BAR */
        .bottom-bar {{
            height: 44px;
            background: rgba(15, 23, 42, 0.9);
            border-top: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 24px;
            flex-shrink: 0;
            z-index: 50;
        }}

        .shortcuts-hint {{
            font-size: 11.5px;
            color: var(--text-dim);
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .key-badge {{
            background: #1e293b;
            border: 1px solid #475569;
            color: #cbd5e1;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: monospace;
            font-size: 10.5px;
            font-weight: 700;
        }}

        .slide-counter-display {{
            font-family: var(--font-display);
            font-size: 13px;
            font-weight: 700;
            color: var(--accent);
        }}
    </style>
</head>
<body>

    <!-- TOP NAVIGATION -->
    <header class="top-bar">
        <div class="brand-area">
            <span class="unit-badge">{unit_badge}</span>
            <div class="slide-title-header">
                <span id="currentSlideName">Loading Slide...</span>
                <span class="stage-pill" id="currentStageName">Stage 1</span>
            </div>
        </div>

        <div class="controls-area">
            <div class="step-progress-indicator" id="stepIndicator"></div>
            <button class="ctrl-btn" onclick="prevStepOrSlide()" title="Left Arrow or Backspace">
                <span>◀ Previous</span>
            </button>
            <button class="ctrl-btn" onclick="nextStepOrSlide()" title="Space or Right Arrow">
                <span>Next ▶</span>
            </button>
            <button class="ctrl-btn" id="prompterToggleBtn" onclick="togglePresenterDrawer()" title="Key P: Toggle Teacher Presenter Teleprompter">
                <span>📋 Presenter Mode</span>
            </button>
            <button class="ctrl-btn" onclick="toggleOverviewModal()" title="Key O or Esc: Slide Directory">
                <span>📑 Slide Directory</span>
            </button>
            <button class="ctrl-btn" onclick="toggleFullscreen()" title="Key F: Fullscreen">
                <span>⛶ Fullscreen</span>
            </button>
        </div>
    </header>

    <!-- MAIN VIEWPORT -->
    <main class="presentation-viewport">
        {slides_html_content}
    </main>

    <!-- BOTTOM CONTROL BAR -->
    <footer class="bottom-bar">
        <div class="shortcuts-hint">
            <span><span class="key-badge">Space</span> / <span class="key-badge">➔</span> Next Step</span>
            <span><span class="key-badge">P</span> Presenter View</span>
            <span><span class="key-badge">F</span> Fullscreen</span>
            <span><span class="key-badge">B</span> Blackout</span>
            <span><span class="key-badge">T</span> Timer</span>
            <span><span class="key-badge">O</span> / <span class="key-badge">Esc</span> Directory</span>
        </div>
        <div class="slide-counter-display" id="slideCounterText">
            Slide 1 / {total_slides}
        </div>
    </footer>

    <!-- TEACHER PRESENTER TELEPROMPTER DRAWER -->
    <aside class="presenter-drawer" id="presenterDrawer">
        <div class="drawer-header">
            <h3><span>👨‍🏫</span> TEACHER TELEPROMPTER & DELIVERY SCRIPT</h3>
            <button class="close-drawer-btn" onclick="togglePresenterDrawer()">&times;</button>
        </div>

        <div class="prompter-section">
            <div class="prompter-label"><span>🗣</span> Verbatim Teacher Talk</div>
            <div class="teacher-talk-text" id="prompterTeacherTalkEn">Loading teacher talk...</div>
            <div class="teacher-talk-vi" id="prompterTeacherTalkVi">Loading guidance...</div>
        </div>

        <div class="prompter-section">
            <div class="prompter-label"><span>👋</span> Physical Gestures & Classroom Movement</div>
            <div class="gesture-box" id="prompterGestures">Loading gestures...</div>
        </div>

        <div class="prompter-section">
            <div class="prompter-label"><span>🎒</span> Expected Student Actions</div>
            <div class="student-action-box" id="prompterStudentAction">Loading student actions...</div>
        </div>

        <div class="prompter-section">
            <div class="prompter-label"><span>📝</span> 3-Column Board Synchronization</div>
            <div class="board-sync-box" id="prompterBoardSync">Loading board notes...</div>
        </div>

        <div class="prompter-section">
            <div class="prompter-label"><span>⏱</span> Interactive Classroom Timer</div>
            <div class="timer-widget">
                <div class="timer-display" id="drawerTimerDisplay">00:00</div>
                <div class="timer-btn-group">
                    <button class="timer-btn" onclick="startCurrentTimer()">Start</button>
                    <button class="timer-btn" onclick="pauseCurrentTimer()">Pause</button>
                    <button class="timer-btn" onclick="resetCurrentTimer()">Reset</button>
                </div>
            </div>
        </div>
    </aside>

    <!-- OVERVIEW MODAL -->
    <div class="overview-modal" id="overviewModal" onclick="handleOverviewBackgroundClick(event)">
        <div class="overview-grid">
            {overview_cards_html}
        </div>
    </div>

    <!-- BLACKOUT SCREEN -->
    <div class="blackout-overlay" id="blackoutOverlay" onclick="toggleBlackout()"></div>

    <!-- JAVASCRIPT ENGINE -->
    <script>
        const slidesData = {slides_json_data};
        let currentSlideIndex = 0;
        let currentStep = 1;
        let timerInterval = null;
        let timerSeconds = 0;
        let timerRunning = false;
        let defaultTimerSeconds = 60;

        document.addEventListener('DOMContentLoaded', () => {{
            showSlide(0, 1);
            setupKeyboardListeners();
        }});

        function showSlide(index, step = 1) {{
            if (index < 0 || index >= slidesData.length) return;
            currentSlideIndex = index;
            currentStep = step;

            const slides = document.querySelectorAll('.slide-canvas');
            slides.forEach((s, idx) => {{
                if (idx === currentSlideIndex) {{
                    s.classList.add('active-slide');
                }} else {{
                    s.classList.remove('active-slide');
                }}
            }});

            const slide = slidesData[currentSlideIndex];
            document.getElementById('currentSlideName').textContent = slide.title;
            document.getElementById('currentStageName').textContent = slide.stage;
            document.getElementById('slideCounterText').textContent = `Slide ${{currentSlideIndex + 1}} / ${{slidesData.length}}`;

            updateStepIndicator(slide.maxSteps, currentStep);
            applyStepBuilds(slide, currentStep);
            updatePrompter(slide);
            setupSlideTimer(slide);
        }}

        function updateStepIndicator(maxSteps, step) {{
            const container = document.getElementById('stepIndicator');
            container.innerHTML = '';
            for (let i = 1; i <= maxSteps; i++) {{
                const dot = document.createElement('div');
                dot.className = 'step-dot' + (i < step ? ' done' : (i === step ? ' active' : ''));
                container.appendChild(dot);
            }}
        }}

        function applyStepBuilds(slide, step) {{
            const currentCanvas = document.querySelector('.slide-canvas.active-slide');
            if (!currentCanvas) return;

            // Handle Target Chunk Slide Builds
            if (slide.type === 'vocab-chunk') {{
                const phoneticsCard = currentCanvas.querySelector('.phonetics-card');
                const writtenCard = currentCanvas.querySelector('.written-form-card');
                const collocCard = currentCanvas.querySelector('.collocation-card');

                // Step 1: Visual only (CCQs dimmed, lexis cards dimmed)
                // Step 2: CCQs questions revealed (answers stay hidden until teacher clicks or triggers!)
                if (step >= 2) {{
                    currentCanvas.querySelectorAll('.ccq-card').forEach((card) => {{
                        card.classList.add('revealed');
                    }});
                }} else {{
                    currentCanvas.querySelectorAll('.ccq-card').forEach((card) => {{
                        card.classList.remove('revealed');
                        const ans = card.querySelector('.ccq-a');
                        if (ans) ans.classList.remove('show-answer');
                    }});
                }}

                // Step 3: Sound & Mumble Drill
                if (step >= 3) {{
                    if (phoneticsCard) phoneticsCard.classList.add('revealed');
                }} else {{
                    if (phoneticsCard) phoneticsCard.classList.remove('revealed');
                }}

                // Step 4: Written Form & Traps
                if (step >= 4) {{
                    if (writtenCard) writtenCard.classList.add('revealed');
                }} else {{
                    if (writtenCard) writtenCard.classList.remove('revealed');
                }}

                // Step 5: Collocation Grid & Personalization
                if (step >= 5) {{
                    if (collocCard) collocCard.classList.add('revealed');
                }} else {{
                    if (collocCard) collocCard.classList.remove('revealed');
                }}
            }} else if (slide.type === 'odd-one-out') {{
                // Step 1: Thinking time. All options neutral.
                // Step 2: Row 1 impostor revealed
                // Step 3: Row 2 impostor revealed
                // Step 4: Row 3 impostor revealed
                const row1Target = currentCanvas.querySelector('#row1-target');
                const row2Target = currentCanvas.querySelector('#row2-target');
                const row3Target = currentCanvas.querySelector('#row3-target');

                if (step >= 2 && row1Target) row1Target.classList.add('revealed');
                else if (row1Target) row1Target.classList.remove('revealed');

                if (step >= 3 && row2Target) row2Target.classList.add('revealed');
                else if (row2Target) row2Target.classList.remove('revealed');

                if (step >= 4 && row3Target) row3Target.classList.add('revealed');
                else if (row3Target) row3Target.classList.remove('revealed');
            }} else if (slide.type === 'practice-clues') {{
                const clues = currentCanvas.querySelectorAll('.clue-target');
                const options = currentCanvas.querySelectorAll('.practice-opt.is-correct');
                if (step >= 2) {{
                    clues.forEach(c => c.classList.add('highlight-clue'));
                }} else {{
                    clues.forEach(c => c.classList.remove('highlight-clue'));
                }}
                if (step >= 3) {{
                    options.forEach(o => o.classList.add('correct-answer'));
                }} else {{
                    options.forEach(o => o.classList.remove('correct-answer'));
                }}
            }} else if (slide.type === 'practice-matrix') {{
                const maskedCells = currentCanvas.querySelectorAll('.masked-cell');
                if (step >= 2) {{
                    maskedCells.forEach(c => c.classList.add('revealed'));
                }} else {{
                    maskedCells.forEach(c => c.classList.remove('revealed'));
                }}
            }} else if (slide.type === 'pragmatics') {{
                const pragCards = currentCanvas.querySelectorAll('.prag-card');
                if (step >= 2) {{
                    pragCards.forEach(c => c.classList.add('revealed'));
                }} else {{
                    pragCards.forEach(c => c.classList.remove('revealed'));
                }}
            }}
        }}

        function nextStepOrSlide() {{
            const slide = slidesData[currentSlideIndex];
            if (currentStep < slide.maxSteps) {{
                currentStep++;
                updateStepIndicator(slide.maxSteps, currentStep);
                applyStepBuilds(slide, currentStep);
            }} else {{
                if (currentSlideIndex < slidesData.length - 1) {{
                    showSlide(currentSlideIndex + 1, 1);
                }}
            }}
        }}

        function prevStepOrSlide() {{
            const slide = slidesData[currentSlideIndex];
            if (currentStep > 1) {{
                currentStep--;
                updateStepIndicator(slide.maxSteps, currentStep);
                applyStepBuilds(slide, currentStep);
            }} else {{
                if (currentSlideIndex > 0) {{
                    const prevSlide = slidesData[currentSlideIndex - 1];
                    showSlide(currentSlideIndex - 1, prevSlide.maxSteps);
                }}
            }}
        }}

        function updatePrompter(slide) {{
            document.getElementById('prompterTeacherTalkEn').innerHTML = `"${{slide.teacherTalkEn}}"`;
            document.getElementById('prompterTeacherTalkVi').innerHTML = slide.teacherTalkVi;
            document.getElementById('prompterGestures').innerHTML = slide.gestures;
            document.getElementById('prompterStudentAction').innerHTML = slide.studentAction;
            document.getElementById('prompterBoardSync').innerHTML = slide.boardSync;
        }}

        function togglePresenterDrawer() {{
            const drawer = document.getElementById('presenterDrawer');
            const btn = document.getElementById('prompterToggleBtn');
            drawer.classList.toggle('open');
            btn.classList.toggle('active');
        }}

        function toggleOverviewModal() {{
            const modal = document.getElementById('overviewModal');
            modal.classList.toggle('open');
            if (modal.classList.contains('open')) {{
                document.querySelectorAll('.overview-card').forEach((c, idx) => {{
                    if (idx === currentSlideIndex) c.classList.add('current-slide');
                    else c.classList.remove('current-slide');
                }});
            }}
        }}

        function handleOverviewBackgroundClick(e) {{
            if (e.target.id === 'overviewModal') toggleOverviewModal();
        }}

        function jumpToSlide(idx) {{
            toggleOverviewModal();
            showSlide(idx, 1);
        }}

        function toggleFullscreen() {{
            if (!document.fullscreenElement) {{
                document.documentElement.requestFullscreen().catch(err => {{}});
            }} else {{
                document.exitFullscreen().catch(err => {{}});
            }}
        }}

        function toggleBlackout() {{
            const blackout = document.getElementById('blackoutOverlay');
            blackout.classList.toggle('active');
        }}

        /* TIMERS */
        function setupSlideTimer(slide) {{
            pauseCurrentTimer();
            defaultTimerSeconds = slide.timerSeconds || 60;
            timerSeconds = defaultTimerSeconds;
            updateTimerDisplay();
        }}

        function startCurrentTimer() {{
            if (timerRunning) return;
            timerRunning = true;
            timerInterval = setInterval(() => {{
                if (timerSeconds > 0) {{
                    timerSeconds--;
                    updateTimerDisplay();
                }} else {{
                    pauseCurrentTimer();
                    playTimerBeep();
                }}
            }}, 1000);
        }}

        function pauseCurrentTimer() {{
            timerRunning = false;
            clearInterval(timerInterval);
        }}

        function resetCurrentTimer() {{
            pauseCurrentTimer();
            timerSeconds = defaultTimerSeconds;
            updateTimerDisplay();
        }}

        function updateTimerDisplay() {{
            const mins = Math.floor(timerSeconds / 60);
            const secs = timerSeconds % 60;
            const str = `${{String(mins).padStart(2, '0')}}:${{String(secs).padStart(2, '0')}}`;
            
            const activeSlideCanvas = document.querySelector('.slide-canvas.active-slide');
            if (activeSlideCanvas) {{
                const slideTimerDisplay = activeSlideCanvas.querySelector('.slide-timer-text');
                if (slideTimerDisplay) slideTimerDisplay.textContent = str;
            }}
            document.getElementById('drawerTimerDisplay').textContent = str;
        }}

        function playTimerBeep() {{
            try {{
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(587.33, ctx.currentTime);
                gain.gain.setValueAtTime(0.3, ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.8);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start();
                osc.stop(ctx.currentTime + 0.8);
            }} catch(e) {{}}
        }}

        /* INTERACTIVE TEACHER ACTIONS */
        function toggleCcqAnswer(cardElement) {{
            const ans = cardElement.querySelector('.ccq-a');
            if (ans) {{
                ans.classList.toggle('show-answer');
                cardElement.classList.add('revealed');
            }}
        }}

        function revealImpostor(rowId) {{
            const target = document.getElementById(rowId);
            if (target) target.classList.toggle('revealed');
        }}

        function revealAllImpostors() {{
            const targets = document.querySelectorAll('.impostor-target');
            targets.forEach(t => t.classList.toggle('revealed'));
        }}

        function toggleClues() {{
            const currentCanvas = document.querySelector('.slide-canvas.active-slide');
            if (!currentCanvas) return;
            currentCanvas.querySelectorAll('.clue-target').forEach(c => c.classList.toggle('highlight-clue'));
        }}

        function togglePracticeAnswers() {{
            const currentCanvas = document.querySelector('.slide-canvas.active-slide');
            if (!currentCanvas) return;
            currentCanvas.querySelectorAll('.practice-opt.is-correct').forEach(o => o.classList.toggle('correct-answer'));
        }}

        function toggleCell(cell) {{
            cell.classList.toggle('revealed');
        }}

        function toggleAllWordFamilyCells() {{
            const currentCanvas = document.querySelector('.slide-canvas.active-slide');
            if (!currentCanvas) return;
            currentCanvas.querySelectorAll('.masked-cell').forEach(c => c.classList.toggle('revealed'));
        }}

        function togglePragmaticsAnalysis() {{
            const currentCanvas = document.querySelector('.slide-canvas.active-slide');
            if (!currentCanvas) return;
            currentCanvas.querySelectorAll('.prag-card').forEach(c => c.classList.toggle('revealed'));
        }}

        /* AUDIO PLAYBACK WITH FALLBACK */
        function playWordAudio(audioPath, fallbackWord) {{
            if (audioPath) {{
                const audio = new Audio(audioPath);
                audio.play().catch(e => {{
                    playSpeechSynthesis(fallbackWord);
                }});
            }} else {{
                playSpeechSynthesis(fallbackWord);
            }}
        }}

        function playSpeechSynthesis(text) {{
            if ('speechSynthesis' in window) {{
                const utter = new SpeechSynthesisUtterance(text);
                utter.lang = 'en-GB';
                utter.rate = 0.9;
                window.speechSynthesis.speak(utter);
            }}
        }}

        function triggerMumbleDrill(seconds = 3) {{
            let remaining = seconds;
            const badge = event.currentTarget;
            const originalText = badge.innerHTML;
            badge.innerHTML = `👄 Silent Mumble: <strong>${{remaining}}s</strong>`;
            
            const interval = setInterval(() => {{
                remaining--;
                if (remaining > 0) {{
                    badge.innerHTML = `👄 Silent Mumble: <strong>${{remaining}}s</strong>`;
                }} else {{
                    clearInterval(interval);
                    badge.innerHTML = `✔ Ready for Choral Drill!`;
                    setTimeout(() => {{ badge.innerHTML = originalText; }}, 2500);
                }}
            }}, 1000);
        }}

        /* KEYBOARD EVENT HANDLERS */
        function setupKeyboardListeners() {{
            document.addEventListener('keydown', (e) => {{
                if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
                
                switch (e.key) {{
                    case 'ArrowRight':
                    case ' ':
                        e.preventDefault();
                        nextStepOrSlide();
                        break;
                    case 'ArrowLeft':
                    case 'Backspace':
                        e.preventDefault();
                        prevStepOrSlide();
                        break;
                    case 'p':
                    case 'P':
                        togglePresenterDrawer();
                        break;
                    case 'f':
                    case 'F':
                        toggleFullscreen();
                        break;
                    case 'b':
                    case 'B':
                        toggleBlackout();
                        break;
                    case 't':
                    case 'T':
                        if (timerRunning) pauseCurrentTimer();
                        else startCurrentTimer();
                        break;
                    case 'r':
                    case 'R':
                        resetCurrentTimer();
                        break;
                    case 'o':
                    case 'O':
                    case 'Escape':
                        toggleOverviewModal();
                        break;
                }}
            }});
        }}
    </script>
</body>
</html>
"""

def generate_slides_data(unit_dir, unit_id):
    """
    Synthesizes the complete 18 slides structure in 100% professional English
    with teacher-controlled answer reveals and responsive layout.
    """
    vocab_file = unit_dir / "vocab.json"
    image_prompts_file = unit_dir / "image-prompts.json"
    
    with open(vocab_file, "r", encoding="utf-8") as f:
        vocab_data = json.load(f)

    image_prompts = {}
    if image_prompts_file.exists():
        with open(image_prompts_file, "r", encoding="utf-8") as f:
            for item in json.load(f):
                image_prompts[item.get("object", "")] = item.get("prompt", "")

    all_words = {}
    for group in vocab_data:
        for w in group.get("words", []):
            all_words[w["english_word"].lower()] = w

    slides = []

    # SLIDE 1: Welcome & Energy Reset
    slides.append({
        "id": 1,
        "title": "Welcome & High-Energy Reset",
        "stage": "Stage 1: Warm-up (00:00 - 00:01)",
        "type": "welcome",
        "maxSteps": 1,
        "timerSeconds": 60,
        "teacherTalkEn": "Good morning, class! Pens down, eyes on me. Take a deep breath. Today we have a high-energy mission: unlocking the secret language codes of real family life. Are you ready?",
        "teacherTalkVi": "Teacher stands at center stage with arms open and direct eye contact. Students sit upright and reply energetically: 'Yes, teacher! Ready!'",
        "gestures": "Stand at stage center, open palms toward the class, maintain a welcoming posture and scan all four corners of the classroom.",
        "studentAction": "100% of students place their pens down, sit straight, focus their attention on the screen and teacher, chanting 'Yes, teacher! Ready!'",
        "boardSync": "Write on Middle Board: 'UNIT 1: FAMILY LIFE - LEXIS FOCUS'.",
        "htmlContent": f"""
        <div class="slide-body-grid single-col" style="align-items: center; justify-content: center; text-align: center;">
            <div style="max-width: 820px; margin: 0 auto; display: flex; flex-direction: column; align-items: center; gap: 20px;">
                <div style="background: rgba(37, 99, 235, 0.2); border: 1px solid rgba(59, 130, 246, 0.5); padding: 6px 18px; border-radius: 9999px; color: #60a5fa; font-weight: 700; font-size: 13px; text-transform: uppercase; letter-spacing: 1px;">
                    Global Success 10 • Unit 1 • Intensive Lexical Mastery
                </div>
                <h1 style="font-family: var(--font-display); font-size: 46px; font-weight: 800; color: #ffffff; line-height: 1.15; letter-spacing: -1px;">
                    FAMILY LIFE:<br><span style="background: linear-gradient(135deg, #38bdf8, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">THE SECRET LANGUAGE CODES</span>
                </h1>
                <p style="font-size: 16px; color: #94a3b8; line-height: 1.5; max-width: 650px;">
                    Mastering 8 Core Lexical Chunks, Natural Collocations & Real-Life Fluency in 60 Minutes.
                </p>
                <div style="display: flex; gap: 16px; margin-top: 6px;">
                    <div style="background: #1e293b; border: 1px solid #334155; padding: 12px 20px; border-radius: 10px; text-align: left;">
                        <span style="display: block; font-size: 11.5px; color: #facc15; font-weight: 700; text-transform: uppercase;">Classroom Standard</span>
                        <strong style="color: #ffffff; font-size: 14px;">Pens Down • Eyes on Screen • Active Recall</strong>
                    </div>
                    <div style="background: #1e293b; border: 1px solid #334155; padding: 12px 20px; border-radius: 10px; text-align: left;">
                        <span style="display: block; font-size: 11.5px; color: #38bdf8; font-weight: 700; text-transform: uppercase;">Cognitive Sequence</span>
                        <strong style="color: #ffffff; font-size: 14px;">Meaning First ➔ Spoken Beat ➔ Real Fluency</strong>
                    </div>
                </div>
            </div>
        </div>
        """
    })

    # SLIDE 2: Odd-One-Out Collocation Blitz (ANSWERS HIDDEN INITIALLY)
    slides.append({
        "id": 2,
        "title": "Odd-One-Out Collocation Blitz",
        "stage": "Stage 1: Warm-up (00:01 - 00:04)",
        "type": "odd-one-out",
        "maxSteps": 4,
        "timerSeconds": 15,
        "teacherTalkEn": "Look at Screen 1! You see 3 rows of collocations. One combination in each row is an impostor. You have 15 seconds to write the non-collocate on your mini-boards. Silent thinking. Go! ... 3, 2, 1 - Boards UP! ... Row 2, Nam, why did you write 'a decision' with DO?",
        "teacherTalkVi": "Teacher clicks timer for 15s. Students write on mini-whiteboards silently. Teacher reveals impostors one row at a time.",
        "gestures": "Click timer button, raise index finger to lips for absolute silence. On countdown 3-2-1, thrust both arms upward calling 'Boards UP!'",
        "studentAction": "Silent reflection for 15s, writing the non-collocate on mini-whiteboards. On cue, all raise boards across their chests.",
        "boardSync": "Write on Left Board: 'DO a decision ➔ MAKE a decision'.",
        "htmlContent": f"""
        <div class="slide-body-grid single-col" style="max-width: 1050px; margin: 0 auto; width: 100%;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 13.5px; color: #facc15; font-weight: 700; text-transform: uppercase;">
                    ⚡ 15-SECOND MINI-WHITEBOARD CHALLENGE: SPOT THE IMPOSTOR (NON-COLLOCATE)
                </span>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div class="timer-widget" style="margin: 0; padding: 3px 10px;">
                        <span class="slide-timer-text" style="font-family: var(--font-display); font-size: 16px; font-weight: 800; color: #facc15;">00:15</span>
                        <button class="timer-btn" onclick="startCurrentTimer()" style="margin-left: 6px;">Start 15s</button>
                    </div>
                    <button class="reveal-action-btn" onclick="revealAllImpostors()">Reveal All</button>
                </div>
            </div>

            <!-- ROW 1 -->
            <div class="practice-question-card">
                <div class="practice-q-text">
                    <span><strong>ROW 1:</strong> Collocating with verb <span style="color: #38bdf8; font-weight: 800;">DO</span></span>
                    <button class="reveal-action-btn" onclick="revealImpostor('row1-target')">Reveal Row 1</button>
                </div>
                <div class="practice-options-grid">
                    <div class="practice-opt"><span>A. housework</span></div>
                    <div class="practice-opt"><span>B. household chores</span></div>
                    <div class="practice-opt"><span>C. the cooking</span></div>
                    <div class="practice-opt impostor-target" id="row1-target">
                        <span>D. a decision</span>
                        <span class="impostor-badge">✘ Impostor! ➔ ✔ MAKE a decision</span>
                    </div>
                </div>
            </div>

            <!-- ROW 2 -->
            <div class="practice-question-card">
                <div class="practice-q-text">
                    <span><strong>ROW 2:</strong> Collocating with verb <span style="color: #38bdf8; font-weight: 800;">SHARE</span></span>
                    <button class="reveal-action-btn" onclick="revealImpostor('row2-target')">Reveal Row 2</button>
                </div>
                <div class="practice-options-grid">
                    <div class="practice-opt"><span>A. housework</span></div>
                    <div class="practice-opt"><span>B. responsibility</span></div>
                    <div class="practice-opt impostor-target" id="row2-target">
                        <span>C. a heavy lifting</span>
                        <span class="impostor-badge">✘ Impostor! ➔ ✔ DO the heavy lifting</span>
                    </div>
                    <div class="practice-opt"><span>D. household duties</span></div>
                </div>
            </div>

            <!-- ROW 3 -->
            <div class="practice-question-card">
                <div class="practice-q-text">
                    <span><strong>ROW 3:</strong> Collocating with verb <span style="color: #38bdf8; font-weight: 800;">MAKE</span></span>
                    <button class="reveal-action-btn" onclick="revealImpostor('row3-target')">Reveal Row 3</button>
                </div>
                <div class="practice-options-grid">
                    <div class="practice-opt"><span>A. breakfast</span></div>
                    <div class="practice-opt"><span>B. an effort</span></div>
                    <div class="practice-opt"><span>C. a choice</span></div>
                    <div class="practice-opt impostor-target" id="row3-target">
                        <span>D. the laundry</span>
                        <span class="impostor-badge">✘ Impostor! ➔ ✔ DO the laundry</span>
                    </div>
                </div>
            </div>
        </div>
        """
    })

    # SLIDE 3: Visual Thematic Hook & Cognitive Priming
    slides.append({
        "id": 3,
        "title": "Visual Thematic Hook & Cognitive Priming",
        "stage": "Stage 1: Warm-up (00:04 - 00:07)",
        "type": "thematic-hook",
        "maxSteps": 2,
        "timerSeconds": 60,
        "teacherTalkEn": "Now, look at these two photos from our cards portal. Photo A: a father returning home tired with a heavy briefcase. Photo B: a family together in the kitchen washing dishes and laughing. Which life looks happier, and who carries the heavier load?",
        "teacherTalkVi": "Teacher invites pair whispers for 10s. Elicits student insights on who earns versus who shares housework.",
        "gestures": "Extend both palms out like balancing scales left and right. Incline body forward encouraging students to share their observations.",
        "studentAction": "Whisper discussion in pairs for 10s. Students volunteer to speak: 'Photo B is happier because they share housework, while in Photo A the father is lonely earning money.'",
        "boardSync": "Write on Middle Board: '1. Who earns? (Breadwinner) vs Who shares? (Housework)'.",
        "htmlContent": f"""
        <div class="slide-body-grid" style="grid-template-columns: 1fr 1fr; gap: 20px; align-items: center;">
            <div style="background: var(--bg-card); border: 2px solid var(--border); border-radius: 12px; overflow: hidden; padding: 14px; display: flex; flex-direction: column; gap: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="background: #2563eb; color: #ffffff; font-weight: 800; font-size: 12px; padding: 3px 9px; border-radius: 6px;">PHOTO A</span>
                    <span style="font-size: 12.5px; color: #94a3b8; font-weight: 600;">Earning & Providing</span>
                </div>
                <div class="image-frame" style="max-height: 250px;">
                    <img src="../../media/gs10/unit-1/images/breadwinner.webp" alt="Working father arriving home" onerror="this.src='/lessons/media/gs10/unit-1/images/breadwinner.webp'">
                </div>
                <div style="font-size: 13px; color: #cbd5e1; line-height: 1.45; background: #0f172a; padding: 8px 12px; border-radius: 6px;">
                    <strong>Context:</strong> A father arriving home late, exhausted with a heavy briefcase, bearing the entire family's financial burden alone.
                </div>
            </div>

            <div style="background: var(--bg-card); border: 2px solid var(--border); border-radius: 12px; overflow: hidden; padding: 14px; display: flex; flex-direction: column; gap: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="background: #10b981; color: #ffffff; font-weight: 800; font-size: 12px; padding: 3px 9px; border-radius: 6px;">PHOTO B</span>
                    <span style="font-size: 12.5px; color: #94a3b8; font-weight: 600;">Sharing & Bonding</span>
                </div>
                <div class="image-frame" style="max-height: 250px;">
                    <img src="../../media/gs10/unit-1/images/housework.webp" alt="Family sharing housework" onerror="this.src='/lessons/media/gs10/unit-1/images/housework.webp'">
                </div>
                <div style="font-size: 13px; color: #cbd5e1; line-height: 1.45; background: #0f172a; padding: 8px 12px; border-radius: 6px;">
                    <strong>Context:</strong> Family members cooperating cheerfully in the kitchen, washing dishes, tidying up, and sharing household responsibilities.
                </div>
            </div>
        </div>
        """
    })

    # SLIDES 4-11: 8 TARGET LEXICAL CHUNKS (ALL ENGLISH + TEACHER-CONTROLLED CCQ REVEAL)
    chunk_specs = [
        {
            "word": "breadwinner",
            "ipa": "/ˈbredwɪnə/",
            "ipa_us": "/ˈbredwɪnər/",
            "beat": "<span class=\"primary\">BREAD</span>-win-ner",
            "pos": "noun",
            "def_en": "The primary wage earner who provides financial support for the entire household.",
            "image": "breadwinner.webp",
            "trap_word": "B R <span class=\"trap-highlight\">E A</span> D W I <span class=\"trap-highlight\">N N</span> E R",
            "trap_alert": "<strong>Spelling Trap:</strong> Vowel sound /e/ is spelled with <u>ea</u> (as in 'bread') • Double consonant <u>nn</u> (winner). Single 'n' is a misspelling!",
            "collocs": ["primary", "sole", "family"],
            "colloc_center": "BREADWINNER",
            "frame": "In my family, <span class=\"fill-spot\">[Person]</span> is the primary breadwinner, while I usually <span class=\"fill-spot\">[Action]</span>.",
            "ccqs": [
                {"q": "Does a breadwinner stay home all day or work to earn money?", "a": "Works to earn money to support the family!"},
                {"q": "Can a mother or wife also be the breadwinner in modern society?", "a": "Yes, absolutely! Both husbands and wives can be breadwinners."},
                {"q": "If ONLY ONE person earns money, what word do we add before it?", "a": "Sole breadwinner / Primary breadwinner."}
            ],
            "teacherEn": "Look at this gentleman on screen. He works 10 hours a day. He buys groceries, pays electricity bills, and supports the whole family. In English, we call this person a BREADWINNER. Let's check our CCQs!",
            "teacherVi": "Teacher points to the image, prompts student predictions, then clicks CCQs one by one to reveal answers after oral response.",
            "gestures": "Gesture opening a wallet and sheltering dependents. Maintain an inquisitive expression, inviting student deductive thinking.",
            "studentAction": "Students inspect the photo, answer CCQs orally, practice 3s Mumble Drill, and underline double 'nn' in their notebooks.",
            "boardSync": "Middle Board: '[sole / primary] + BREADWINNER'. Left Board: 'breadwinner (double n)'."
        },
        {
            "word": "homemaker",
            "ipa": "/ˈhəʊmmeɪkə/",
            "ipa_us": "/ˈhoʊmmeɪkər/",
            "beat": "<span class=\"primary\">HOME</span>-ma-ker",
            "pos": "noun",
            "def_en": "A person who manages a home and takes care of domestic chores and family members.",
            "image": "homemaker.webp",
            "trap_word": "H O <span class=\"trap-highlight\">M E M</span> A K E R",
            "trap_alert": "<strong>Spelling Trap:</strong> Solid compound noun (home + maker, no space). Notice double <u>m</u> across the compound boundary.",
            "collocs": ["full-time", "dedicated", "modern"],
            "colloc_center": "HOMEMAKER",
            "frame": "Being a homemaker is just as demanding as an office job because <span class=\"fill-spot\">[Reason]</span>.",
            "ccqs": [
                {"q": "Does a homemaker work in a corporate office or manage the household?", "a": "Manages domestic tasks and cares for family members at home!"},
                {"q": "Is homemaking simple leisure or does it require continuous dedication?", "a": "Requires immense dedication, time, and hard daily work!"},
                {"q": "Can a man be a homemaker in modern life?", "a": "Yes! A stay-at-home father or househusband."}
            ],
            "teacherEn": "Now look at the kitchen. While the breadwinner earns money outside, this person manages meals, cleaning, and child care with great devotion. What is this crucial role? HOMEMAKER!",
            "teacherVi": "Teacher demonstrates organizing kitchen duties, highlights the gender-neutral status of modern homemakers.",
            "gestures": "Mimic arranging plates and caring for household items. Emphasize equal dignity between breadwinning and homemaking.",
            "studentAction": "Students contrast breadwinner and homemaker, asserting the equal value of domestic contributions.",
            "boardSync": "Middle Board: '[full-time / dedicated] + HOMEMAKER'."
        },
        {
            "word": "housework",
            "ipa": "/ˈhaʊswɜːk/",
            "ipa_us": "/ˈhaʊswɜːrk/",
            "beat": "<span class=\"primary\">HOUSE</span>-work",
            "pos": "noun",
            "def_en": "Work that people do to keep their house clean and tidy (uncountable noun).",
            "image": "housework.webp",
            "trap_word": "H O U S E W O R K <span class=\"trap-highlight\">(UNCOUNTABLE!)</span>",
            "trap_alert": "<strong>Grammar Trap:</strong> UNCOUNTABLE NOUN! Never say '*three houseworks' or '*a housework'. The collocate verb is strictly DO!",
            "collocs": ["do", "share", "help with"],
            "colloc_center": "HOUSEWORK",
            "frame": "In our family, we always <span class=\"fill-spot\">share the housework</span> so nobody feels overwhelmed.",
            "ccqs": [
                {"q": "Is housework done for school or for keeping the home clean?", "a": "For keeping the house clean! (Homework is for school)."},
                {"q": "Can we say 'I have three houseworks to do'?", "a": "NO! Housework is uncountable. Never add -s!"},
                {"q": "Which de-lexicalised verb pairs with housework: MAKE or DO?", "a": "DO housework! (Never say make housework)."}
            ],
            "teacherEn": "Notice this critical distinction: Homework is for school; HOUSEWORK is for keeping your house clean! And remember Golden Rule #1: You DO housework, you never MAKE it!",
            "teacherVi": "Teacher slashes an imaginary '-s' in the air, stressing that housework is uncountable and pairs with DO.",
            "gestures": "Firmly wave hands in an 'X' shape to prohibit saying '*houseworks'. Point to the collocate DO.",
            "studentAction": "Class chorally chants: 'DO housework, NOT make housework! Uncountable!'",
            "boardSync": "Middle Board: '[do / share] + HOUSEWORK (Uncountable)'. Left Board: 'NO houseworks!'."
        },
        {
            "word": "household chore",
            "ipa": "/ˈhaʊshəʊld tʃɔː/",
            "ipa_us": "/ˈhaʊshoʊld tʃɔːr/",
            "beat": "<span class=\"primary\">HOUSE</span>-hold <span class=\"primary\">CHORE</span>",
            "pos": "noun",
            "def_en": "A routine daily domestic task, such as sweeping, dusting, or washing dishes (countable).",
            "image": "household-chore.webp",
            "trap_word": "H O U S E H O L D &nbsp; C H O R <span class=\"trap-highlight\">E (Countable)</span>",
            "trap_alert": "<strong>Spelling & Grammar:</strong> Two separate words. 'chore' starts with /tʃ/ spelled 'ch' and ends with silent 'e'. Countable: chores.",
            "collocs": ["daily", "routine", "split"],
            "colloc_center": "HOUSEHOLD CHORES",
            "frame": "My daily household chore is <span class=\"fill-spot\">[sweeping / washing dishes]</span> every afternoon.",
            "ccqs": [
                {"q": "Is a chore a rare annual project or a routine daily task?", "a": "A routine, regular daily duty (sweeping, dusting, taking out rubbish)."},
                {"q": "Is 'chore' countable? Can we say 'household chores'?", "a": "Yes! Countable: one chore, many household chores."},
                {"q": "What verbs pair naturally with household chores?", "a": "DO household chores / SPLIT household chores."}
            ],
            "teacherEn": "Look at the young boy sweeping the wooden floor. Sweeping is a routine daily task. We call this a HOUSEHOLD CHORE. Notice that unlike housework, chores are COUNTABLE!",
            "teacherVi": "Teacher demonstrates sweeping floors and emptying dustpans, emphasizing that chores take plural '-s'.",
            "gestures": "Mimic holding a broom and sweeping dust into a dustpan. Trace plural '-s' on board.",
            "studentAction": "Students contrast 'housework (uncountable)' versus 'household chores (countable)' in their lexical notebooks.",
            "boardSync": "Middle Board: '[daily / routine] + HOUSEHOLD CHORES'."
        },
        {
            "word": "heavy lifting",
            "ipa": "/ˌhevi ˈlɪftɪŋ/",
            "ipa_us": "/ˌhevi ˈlɪftɪŋ/",
            "beat": "hea-vy <span class=\"primary\">LIF</span>-ting",
            "pos": "noun",
            "def_en": "The physical moving of bulky heavy objects; also metaphorically the hardest part of a task.",
            "image": "heavy-lifting.webp",
            "trap_word": "H <span class=\"trap-highlight\">E A</span> V Y &nbsp; L I F T I N G",
            "trap_alert": "<strong>Pronunciation & Form:</strong> 'heavy' sound /e/ is spelled with <u>ea</u>. Collocates with the definite article: DO THE HEAVY LIFTING.",
            "collocs": ["do", "handle", "leave"],
            "colloc_center": "THE HEAVY LIFTING",
            "frame": "Whenever my family rearranges furniture, my brother <span class=\"fill-spot\">handles the heavy lifting</span>.",
            "ccqs": [
                {"q": "Does heavy lifting mean picking up light papers or moving bulky boxes?", "a": "Moving bulky, heavy furniture or appliances!"},
                {"q": "Can it metaphorically mean doing the hardest part of a difficult task?", "a": "Yes! Handling the most demanding work."},
                {"q": "What verb collocates: DO or MAKE the heavy lifting?", "a": "DO the heavy lifting!"}
            ],
            "teacherEn": "Look at this safe lifting posture! Hoisting a 20kg box from the ground. When rearranging home furniture, who takes this burden? In English: DO THE HEAVY LIFTING!",
            "teacherVi": "Teacher mimics squatting safely to lift a heavy container, clicking to elicit student oral responses.",
            "gestures": "Flex arms demonstrating safe lifting posture. Tap leg on the accented syllable 'LIF'.",
            "studentAction": "Students articulate 'DO THE HEAVY LIFTING' with primary stress beat on 'LIF'.",
            "boardSync": "Middle Board: 'do the heavy lifting'."
        },
        {
            "word": "do the cooking",
            "ipa": "/duː ðə ˈkʊkɪŋ/",
            "ipa_us": "/duː ðə ˈkʊkɪŋ/",
            "beat": "do the <span class=\"primary\">COOK</span>-ing",
            "pos": "phrase",
            "def_en": "The activity or duty of preparing and cooking meals for the family.",
            "image": "do-the-cooking.webp",
            "trap_word": "D O &nbsp; T H E &nbsp; C <span class=\"trap-highlight\">O O</span> K I N G",
            "trap_alert": "<strong>Phrasal Trap:</strong> Requires the definite article 'the' (do THE cooking). Double 'oo' is short vowel /ʊ/.",
            "collocs": ["help with", "take turns to", "love to"],
            "colloc_center": "DO THE COOKING",
            "frame": "On weekends, my dad loves to <span class=\"fill-spot\">do the cooking</span> and prepares special dishes.",
            "ccqs": [
                {"q": "Does 'do the cooking' mean eating meals or preparing food over the stove?", "a": "Preparing and cooking meals in the kitchen!"},
                {"q": "Which verb is required: MAKE the cooking or DO the cooking?", "a": "DO the cooking! (Always DO)."},
                {"q": "Can family members take turns to do the cooking?", "a": "Yes! Take turns to do the cooking."}
            ],
            "teacherEn": "Sautéing fresh peppers in a hot skillet! Preparing dinner for the household. We say: DO THE COOKING. Never say 'make the cooking'!",
            "teacherVi": "Teacher demonstrates sautéing vegetables in a pan, checks CCQs before revealing written phrase.",
            "gestures": "Stir an imaginary wooden spatula in a hot frying pan, savoring the aroma.",
            "studentAction": "Students practice sentence frame: 'My mother does the cooking, but my father helps with the preparation.'",
            "boardSync": "Middle Board: 'take turns to do the cooking'."
        },
        {
            "word": "do the laundry",
            "ipa": "/duː ðə ˈlɔːndri/",
            "ipa_us": "/duː ðə ˈlɔːndri/",
            "beat": "do the <span class=\"primary\">LAUN</span>-dry",
            "pos": "phrase",
            "def_en": "The chore of washing dirty clothes, linens, and drying or folding them.",
            "image": "do-the-laundry.webp",
            "trap_word": "D O &nbsp; T H E &nbsp; L <span class=\"trap-highlight\">A U</span> N D R Y",
            "trap_alert": "<strong>Spelling Trap:</strong> 'laundry' features vowel digraph <u>au</u> (/ɔː/) and ends with 'dry'. Always pairs with DO.",
            "collocs": ["sort", "fold", "hang out"],
            "colloc_center": "DO THE LAUNDRY",
            "frame": "I usually <span class=\"fill-spot\">do the laundry</span> twice a week and hang the clothes to dry.",
            "ccqs": [
                {"q": "Does doing the laundry mean washing dirty plates or washing dirty clothes?", "a": "Washing dirty clothes, towels, and bedsheets!"},
                {"q": "What verb is used: DO or MAKE the laundry?", "a": "DO the laundry!"},
                {"q": "What household machine helps us do the laundry?", "a": "A washing machine!"}
            ],
            "teacherEn": "Carrying a wicker basket of fresh wash to the drying rack! In English, cleaning clothes is: DO THE LAUNDRY!",
            "teacherVi": "Teacher mimics carrying a laundry basket, elicits collocations like sort, fold, hang out.",
            "gestures": "Mimic holding a full basket and clipping fresh clothes to a clothesline.",
            "studentAction": "Students record collocations: 'do the laundry, fold the laundry, sort the laundry'.",
            "boardSync": "Middle Board: 'do the laundry ➔ fold / hang out'."
        },
        {
            "word": "do the washing-up",
            "ipa": "/duː ðə ˌwɒʃɪŋ ˈʌp/",
            "ipa_us": "/duː ðə ˈwɑːʃɪŋ ʌp/",
            "beat": "do the wash-ing <span class=\"primary\">UP</span>",
            "pos": "phrase",
            "def_en": "The chore of cleaning dishes, cutlery, and cooking utensils after a meal (British English).",
            "image": "do-the-washing-up.webp",
            "trap_word": "D O &nbsp; T H E &nbsp; W A S H I N G <span class=\"trap-highlight\">- U P</span>",
            "trap_alert": "<strong>Register & Form:</strong> British English uses hyphen 'washing-up'. American English uses 'do the dishes / wash the dishes'.",
            "collocs": ["help with", "stack plates for", "take turns to"],
            "colloc_center": "DO THE WASHING-UP",
            "frame": "Whoever finishes dinner last in our home has to <span class=\"fill-spot\">do the washing-up</span>!",
            "ccqs": [
                {"q": "Does washing-up mean taking a body shower or cleaning dirty dinner plates?", "a": "Cleaning dinner plates, cutlery, cups, and pots!"},
                {"q": "In American English, what is the exact equivalent phrase?", "a": "Do the dishes / wash the dishes!"},
                {"q": "Who should do the washing-up after meals?", "a": "Family members should take turns or do it together!"}
            ],
            "teacherEn": "Yellow rubber gloves, soapy sponges, and sparkling ceramic plates! British English: DO THE WASHING-UP. American English: DO THE DISHES!",
            "teacherVi": "Teacher demonstrates scrubbing dishes and highlights the UK/US vocabulary divergence.",
            "gestures": "Mimic scrubbing a plate with a sponge and placing it on a drying rack.",
            "studentAction": "Students rehearse the comparison: 'do the washing-up (UK) = do the dishes (US)'.",
            "boardSync": "Middle Board: 'do the washing-up (UK) = do the dishes (US)'."
        }
    ]

    for idx, chunk in enumerate(chunk_specs):
        s_id = idx + 4
        ccq_html = ""
        for q_idx, c in enumerate(chunk["ccqs"]):
            ccq_html += f"""
            <div class="ccq-card" onclick="toggleCcqAnswer(this)">
                <div class="ccq-q">
                    <div class="ccq-q-left">
                        <span class="ccq-q-num">CCQ {q_idx + 1}</span>
                        <span>{c['q']}</span>
                    </div>
                    <button class="reveal-hint-btn">Show Key</button>
                </div>
                <div class="ccq-a">
                    <span style="color: #10b981; font-weight: 800;">✔</span> {c['a']}
                </div>
            </div>
            """

        colloc_items_html = "".join([f'<div class="colloc-item">[{c}]</div>' for c in chunk["collocs"]])

        slides.append({
            "id": s_id,
            "title": f"Target Chunk {idx + 1}: {chunk['word'].upper()}",
            "stage": f"Stage 2: Lexis Acquisition ({chunk['word']})",
            "type": "vocab-chunk",
            "maxSteps": 5,
            "timerSeconds": 60,
            "imagePath": f"/lessons/media/gs10/unit-1/images/{chunk['image']}",
            "imageDesc": image_prompts.get(chunk['word'], ""),
            "ccqsList": chunk["ccqs"],
            "phonetics": {
                "ipa": chunk["ipa"],
                "beat": chunk["beat"],
                "audio": f"/lessons/media/gs10/unit-1/audio/{chunk['word'].replace(' ', '-')}.mp3"
            },
            "spellingTrap": {
                "word": chunk["word"].upper(),
                "alert": chunk["trap_alert"]
            },
            "collocationInfo": {
                "collocs": chunk["collocs"],
                "center": chunk["colloc_center"],
                "frame": chunk["frame"]
            },
            "teacherTalkEn": chunk["teacherEn"],
            "teacherTalkVi": chunk["teacherVi"],
            "gestures": chunk["gestures"],
            "studentAction": chunk["studentAction"],
            "boardSync": chunk["boardSync"],
            "htmlContent": f"""
            <div class="slide-body-grid">
                <!-- LEFT COLUMN: VISUAL CONTEXT & CCQS -->
                <div class="visual-col">
                    <div class="image-frame">
                        <img src="../../media/gs10/unit-1/images/{chunk['image']}" alt="{chunk['word']}" onerror="this.src='/lessons/media/gs10/unit-1/images/{chunk['image']}'">
                    </div>
                    <div class="image-caption-box">
                        <strong>Visual Context:</strong>
                        <span>Real-world visual representation of the core concept.</span>
                    </div>
                    <div class="ccq-container">
                        <div class="ccq-title-badge">
                            <span>🔍 CONCEPT CHECKING QUESTIONS (CCQS)</span>
                            <span style="font-size: 11px; color: #94a3b8;">Click card to toggle answer</span>
                        </div>
                        {ccq_html}
                    </div>
                </div>

                <!-- RIGHT COLUMN: FORM, PHONETICS, COLLOCATION -->
                <div class="lexis-col">
                    <!-- PHONETICS (STEP 3) -->
                    <div class="phonetics-card">
                        <div class="ipa-wrap">
                            <span class="ipa-text">{chunk['ipa']} <span style="font-size: 14px; color: #94a3b8; font-weight: 500;">(UK)</span></span>
                            <div class="stress-beat">
                                <span>Stress Rhythm:</span>
                                <strong>{chunk['beat']}</strong>
                            </div>
                        </div>
                        <div class="audio-actions">
                            <button class="play-audio-btn" onclick="playWordAudio('/lessons/media/gs10/unit-1/audio/{chunk['word'].replace(' ', '-')}.mp3', '{chunk['word']}')" title="Play Native Audio">
                                🔊
                            </button>
                            <div class="mumble-drill-badge" onclick="triggerMumbleDrill(3)">
                                <span>👄 Mumble Drill: <strong>3s</strong></span>
                            </div>
                        </div>
                    </div>

                    <!-- WRITTEN FORM & TRAPS (STEP 4) -->
                    <div class="written-form-card">
                        <div class="headword-banner">
                            <h3 class="headword">{chunk['trap_word']}</h3>
                            <span class="definition-en">({chunk['pos']}): {chunk['def_en']}</span>
                        </div>
                        <div class="spelling-trap-alert">
                            {chunk['trap_alert']}
                        </div>
                    </div>

                    <!-- COLLOCATION GRID & SENTENCE FRAME (STEP 5) -->
                    <div class="collocation-card">
                        <div class="collocation-grid-display">
                            <div class="colloc-left-branch">
                                {colloc_items_html}
                            </div>
                            <div style="font-size: 18px; color: #38bdf8;">➔</div>
                            <div class="colloc-center-word">
                                {chunk['colloc_center']}
                            </div>
                        </div>

                        <div class="sentence-frame-box">
                            <h5>Personalised Sentence Frame</h5>
                            <div class="frame-text">
                                "{chunk['frame']}"
                            </div>
                        </div>

                        <div class="timer-widget">
                            <div class="timer-display">
                                <span>⏱ 60s Challenge:</span>
                                <span class="slide-timer-text">01:00</span>
                            </div>
                            <div class="timer-btn-group">
                                <button class="timer-btn" onclick="startCurrentTimer()">Start</button>
                                <button class="timer-btn" onclick="pauseCurrentTimer()">Pause</button>
                                <button class="timer-btn" onclick="resetCurrentTimer()">Reset</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """
        })

    # SLIDE 12: Controlled Practice: Clue Underlining (ANSWERS HIDDEN INITIALLY)
    slides.append({
        "id": 12,
        "title": "Speed Collocation & Clue Underlining",
        "stage": "Stage 3: Controlled Practice (00:25 - 00:31)",
        "type": "practice-clues",
        "maxSteps": 3,
        "timerSeconds": 60,
        "teacherTalkEn": "Open Handout Page 1 (Exercise 2 & 6). We have 4 questions on screen. Mandatory Rule: You cannot just guess A, B, C, or D! You MUST circle the 'Partner Clue' in the sentence that demands that word. 60 seconds pair discussion with your shoulder partner. Go!",
        "teacherTalkVi": "Teacher instructs students to circle partner clues. Answers remain hidden until teacher activates clue highlight or answers.",
        "gestures": "Interlock fingers modeling pair collaboration. Walk through aisles observing student partner work, then trigger clue underlines.",
        "studentAction": "Students discuss with shoulder partner for 60s, underlining partner clues on their handouts.",
        "boardSync": "Left Board: 'Rule: Always circle the partner clue!'.",
        "htmlContent": f"""
        <div class="slide-body-grid single-col" style="max-width: 1050px; margin: 0 auto; width: 100%;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span style="font-size: 13.5px; color: #38bdf8; font-weight: 700; text-transform: uppercase;">
                    🎯 THINK-PAIR-SHARE: IDENTIFY & CIRCLE THE COLLOCATION PARTNER CLUE (60 SECONDS)
                </span>
                <div style="display: flex; gap: 8px;">
                    <button class="reveal-action-btn" onclick="toggleClues()">🔍 Toggle Clues</button>
                    <button class="reveal-action-btn" onclick="togglePracticeAnswers()">✔ Toggle Answers</button>
                </div>
            </div>

            <div class="practice-question-card">
                <div class="practice-q-text">
                    <span>1. My father works 12 hours a day as the primary [ ? ] to <span class="clue-target">support our entire family</span>.</span>
                </div>
                <div class="practice-options-grid">
                    <div class="practice-opt is-correct"><span>A. breadwinner</span> <strong style="color: #10b981; display: none;" class="check-mark">✔</strong></div>
                    <div class="practice-opt"><span>B. homemaker</span></div>
                    <div class="practice-opt"><span>C. supporter</span></div>
                    <div class="practice-opt"><span>D. servant</span></div>
                </div>
            </div>

            <div class="practice-question-card">
                <div class="practice-q-text">
                    <span>2. When <span class="clue-target">rearranging heavy oak cupboards</span>, my elder brother always handles all the [ ? ].</span>
                </div>
                <div class="practice-options-grid">
                    <div class="practice-opt"><span>A. housework</span></div>
                    <div class="practice-opt is-correct"><span>B. heavy lifting</span> <strong style="color: #10b981; display: none;" class="check-mark">✔</strong></div>
                    <div class="practice-opt"><span>C. household chores</span></div>
                    <div class="practice-opt"><span>D. washing-up</span></div>
                </div>
            </div>

            <div class="practice-question-card">
                <div class="practice-q-text">
                    <span>3. After everyone finishes dinner, my sister and I take turns to do the [ ? ] so our parents can rest.</span>
                </div>
                <div class="practice-options-grid">
                    <div class="practice-opt"><span>A. cooking</span></div>
                    <div class="practice-opt"><span>B. laundry</span></div>
                    <div class="practice-opt is-correct"><span>C. washing-up</span> <strong style="color: #10b981; display: none;" class="check-mark">✔</strong></div>
                    <div class="practice-opt"><span>D. groceries</span></div>
                </div>
            </div>

            <div class="practice-question-card">
                <div class="practice-q-text">
                    <span>4. In a modern family, husband and wife should equally [ ? ] the household chores.</span>
                </div>
                <div class="practice-options-grid">
                    <div class="practice-opt"><span>A. make</span></div>
                    <div class="practice-opt is-correct"><span>B. share</span> <strong style="color: #10b981; display: none;" class="check-mark">✔</strong></div>
                    <div class="practice-opt"><span>C. take</span></div>
                    <div class="practice-opt"><span>D. hold</span></div>
                </div>
            </div>
        </div>
        """
    })

    # SLIDE 13: Morphology & Word Family Matrix (MASKED INITIALLY)
    slides.append({
        "id": 13,
        "title": "Morphology & Word Family Matrix",
        "stage": "Stage 3: Controlled Practice (00:31 - 00:36)",
        "type": "practice-matrix",
        "maxSteps": 2,
        "timerSeconds": 90,
        "teacherTalkEn": "Look at the Word Family Tree on screen from Exercise 13. One root word generates 3 family members! Fill in the missing boxes in 90 seconds: Verb [support] ➔ Noun (Person) [?] ➔ Adjective [?]. Ready, set, write!",
        "teacherTalkVi": "Teacher points to tree diagram on Middle Board. Cells remain masked until teacher triggers reveal.",
        "gestures": "Gesture branching family branches outward. Emphasize Paul Nation's principle that 1 root word triples learning retention.",
        "studentAction": "Students complete the morphology matrix in their lexical notebooks in 90 seconds.",
        "boardSync": "Middle Board: 'support ➔ supporter ➔ supportive'.",
        "htmlContent": f"""
        <div class="slide-body-grid single-col" style="max-width: 1050px; margin: 0 auto; width: 100%;">
            <div style="margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 13.5px; color: #facc15; font-weight: 700; text-transform: uppercase;">
                    🌳 PAUL NATION'S WORD FAMILY TREE (TRIPLES RETENTION EFFICIENCY)
                </span>
                <div style="display: flex; gap: 8px;">
                    <button class="reveal-action-btn" onclick="toggleAllWordFamilyCells()">👁️ Reveal All Cells</button>
                    <span style="font-size: 12.5px; color: #94a3b8;">Time: 90 Seconds</span>
                </div>
            </div>

            <div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: 10px; overflow: hidden;">
                <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 14px;">
                    <thead>
                        <tr style="background: #1e3a8a; color: #ffffff; border-bottom: 2px solid #3b82f6;">
                            <th style="padding: 11px 16px;">ROOT WORD</th>
                            <th style="padding: 11px 16px;">VERB FORM</th>
                            <th style="padding: 11px 16px;">NOUN FORM</th>
                            <th style="padding: 11px 16px;">ADJECTIVE FORM</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="border-bottom: 1px solid #334155;">
                            <td style="padding: 12px 16px; font-weight: 800; color: #38bdf8;">SUPPORT</td>
                            <td style="padding: 12px 16px; color: #ffffff;">support (v)</td>
                            <td style="padding: 12px 16px;">
                                <span class="masked-cell" onclick="toggleCell(this)">supporter (person) / support (concept)</span>
                            </td>
                            <td style="padding: 12px 16px;">
                                <span class="masked-cell" onclick="toggleCell(this)">supportive (adj)</span>
                            </td>
                        </tr>
                        <tr style="border-bottom: 1px solid #334155;">
                            <td style="padding: 12px 16px; font-weight: 800; color: #38bdf8;">RESPONSIBLE</td>
                            <td style="padding: 12px 16px; color: #ffffff;">take responsibility</td>
                            <td style="padding: 12px 16px;">
                                <span class="masked-cell" onclick="toggleCell(this)">responsibility (n)</span>
                            </td>
                            <td style="padding: 12px 16px;">
                                <span class="masked-cell" onclick="toggleCell(this)">responsible (opp: irresponsible)</span>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 16px; font-weight: 800; color: #38bdf8;">DIVIDE</td>
                            <td style="padding: 12px 16px; color: #ffffff;">divide / split</td>
                            <td style="padding: 12px 16px;">
                                <span class="masked-cell" onclick="toggleCell(this)">division (n)</span>
                            </td>
                            <td style="padding: 12px 16px;">
                                <span class="masked-cell" onclick="toggleCell(this)">divisible (adj)</span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div style="margin-top: 12px; background: rgba(30, 41, 59, 0.8); border-left: 4px solid #facc15; padding: 10px 16px; border-radius: 0 6px 6px 0; font-size: 13px; color: #cbd5e1;">
                <strong>💡 Pedagogical Insight:</strong> Click individual cells or use Step builds to reveal answers after students attempt in their notebooks!
            </div>
        </div>
        """
    })

    # SLIDE 14: Real-World Pragmatics / Signs & Notices
    slides.append({
        "id": 14,
        "title": "Real-World Pragmatics / Signs & Notices",
        "stage": "Stage 3: Controlled Practice (00:36 - 00:40)",
        "type": "pragmatics",
        "maxSteps": 2,
        "timerSeconds": 60,
        "teacherTalkEn": "Look at Screen 3 (Exercise 12): A notice on an apartment noticeboard: 'PLEASE PUT OUT THE RUBBISH BEFORE 8 P.M. AND SEPARATE RECYCLABLES.' Who wrote this, and where do you see it in real life?",
        "teacherTalkVi": "Teacher asks students to analyze the real-life sender, tone, and collocation chunks before revealing analysis.",
        "gestures": "Mimic reading an elevator bulletin board poster, analyzing official civic tone.",
        "studentAction": "Students think for 15s. Tuan volunteers: 'It is written by the building management to all apartment residents.'",
        "boardSync": "Left Board: 'Notice Register: Polite Imperative (Civic duty)'.",
        "htmlContent": f"""
        <div class="slide-body-grid" style="grid-template-columns: 1.1fr 1fr; gap: 24px; align-items: center;">
            <div style="background: #ffffff; color: #0f172a; border-radius: 12px; padding: 22px; box-shadow: 0 15px 35px rgba(0,0,0,0.5); border: 4px solid #dc2626;">
                <div style="border-bottom: 2px solid #0f172a; padding-bottom: 10px; margin-bottom: 14px; text-align: center;">
                    <span style="font-size: 11px; font-weight: 800; color: #dc2626; letter-spacing: 1px; text-transform: uppercase;">Building Management Notice</span>
                    <h3 style="font-family: var(--font-display); font-size: 19px; font-weight: 800; margin-top: 2px;">RESIDENTIAL COMMUNITY NOTICE</h3>
                </div>
                <div style="font-family: var(--font-body); font-size: 14.5px; line-height: 1.55; margin-bottom: 14px;">
                    "PLEASE <strong>PUT OUT THE RUBBISH</strong> BEFORE 8:00 P.M. DAILY AND SEPARATE RECYCLABLE MATERIALS INTO THE GREEN BINS.<br><br>
                    DO NOT LEAVE BULKY WASTE OR LAUNDRY ITEMS IN CORRIDORS."
                </div>
                <div style="font-size: 11px; color: #64748b; text-align: right; border-top: 1px dashed #cbd5e1; padding-top: 6px;">
                    Apartment Board of Directors • Green Living Initiative
                </div>
            </div>

            <div style="display: flex; flex-direction: column; gap: 10px;">
                <div style="display: flex; justify-content: flex-end;">
                    <button class="reveal-action-btn" onclick="togglePragmaticsAnalysis()">👁️ Toggle Analysis</button>
                </div>
                <div class="practice-question-card prag-card">
                    <span style="color: #38bdf8; font-weight: 700; font-size: 12px; text-transform: uppercase;">1. Author / Sender</span>
                    <p style="color: #ffffff; font-size: 13.5px; margin-top: 3px;">Building Management Committee addressing all residential tenants.</p>
                </div>
                <div class="practice-question-card prag-card">
                    <span style="color: #facc15; font-weight: 700; font-size: 12px; text-transform: uppercase;">2. Register & Tone</span>
                    <p style="color: #ffffff; font-size: 13.5px; margin-top: 3px;">Formal and authoritative yet polite public imperative (Civic responsibility).</p>
                </div>
                <div class="practice-question-card prag-card">
                    <span style="color: #10b981; font-weight: 700; font-size: 12px; text-transform: uppercase;">3. Target Lexical Chunks</span>
                    <p style="color: #ffffff; font-size: 13.5px; margin-top: 3px;"><strong>PUT OUT THE RUBBISH</strong> & <strong>SEPARATE RECYCLABLES</strong>.</p>
                </div>
            </div>
        </div>
        """
    })

    # SLIDE 15: Cascade 3-Part Exchange
    slides.append({
        "id": 15,
        "title": "Cascade 3-Part Exchange (Prefabricated Chunk Flow)",
        "stage": "Stage 4: Meaning-Focused Output (00:40 - 00:46)",
        "type": "cascade-dialogue",
        "maxSteps": 3,
        "timerSeconds": 60,
        "teacherTalkEn": "Michael Lewis taught us that conversation flows in prefabricated chunks. Look at this Cascade 3-Part Exchange model: Partner A initiates with a problem; Partner B responds focusing on themself [I-focus]; Partner A follows up focusing on Partner B [You-focus]. Let's demonstrate with Huy!",
        "teacherTalkVi": "Teacher demonstrates with a student volunteer, then pairs practice standing face-to-face.",
        "gestures": "Act as Partner A with a busy expression, point to imaginary chores, nod warmly when Partner B responds.",
        "studentAction": "100% of students stand, face their shoulder partner, and alternate roles A and B for 6 minutes.",
        "boardSync": "Right Board: 'Cascade 3-Part: A: Problem ➔ B: I-focus ➔ A: You-focus'.",
        "htmlContent": f"""
        <div class="slide-body-grid single-col" style="max-width: 1000px; margin: 0 auto; width: 100%;">
            <div style="margin-bottom: 6px;">
                <span style="font-size: 13px; color: #38bdf8; font-weight: 700; text-transform: uppercase;">
                    🗣 PREFABRICATED CONVERSATION CHUNKS (3-TURN CASCADE FLOW)
                </span>
            </div>

            <div class="cascade-flow">
                <div class="turn-bubble partner-a">
                    <span class="speaker-badge a">TURN 1: PARTNER A</span>
                    <div class="dialogue-content">
                        <strong>Problem Initiator / Overload:</strong><br>
                        "The living room is completely cluttered, and I still have to <strong class="chunk-highlight">do the laundry</strong> before 6 P.M.!"
                    </div>
                </div>

                <div class="turn-bubble partner-b">
                    <span class="speaker-badge b">TURN 2: PARTNER B</span>
                    <div class="dialogue-content">
                        <strong>I-Focus Solution / Direct Offer:</strong><br>
                        "Don't worry, Mom! <strong>I'll take care of the living room</strong> and <strong class="chunk-highlight">do the heavy lifting</strong> right now."
                    </div>
                </div>

                <div class="turn-bubble partner-a">
                    <span class="speaker-badge a">TURN 3: PARTNER A</span>
                    <div class="dialogue-content">
                        <strong>You-Focus Gratitude & Extension:</strong><br>
                        "Thanks a million! <strong>Could you also help me</strong> <strong class="chunk-highlight">do the washing-up</strong> after dinner tonight?"
                    </div>
                </div>
            </div>

            <div style="margin-top: 12px; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; padding: 10px 16px; color: #a7f3d0; font-size: 13px;">
                <strong>Fluency Rules:</strong> Maintain steady eye contact • Use natural facial expressions • Freely substitute target chunks (do the cooking, household chore).
            </div>
        </div>
        """
    })

    # SLIDE 16: Communicative Task: '1-Minute Fluency Pitch'
    slides.append({
        "id": 16,
        "title": "Communicative Task: '1-Minute Fluency Pitch'",
        "stage": "Stage 4: Meaning-Focused Output (00:46 - 00:54)",
        "type": "communicative-task",
        "maxSteps": 1,
        "timerSeconds": 180,
        "teacherTalkEn": "Final Communicative Mission! In groups of 3, create a 60-second 'Family Chore Charter' for a modern Vietnamese family. Condition: You MUST use at least 3 target chunks from today (breadwinner, share housework, heavy lifting, do the cooking, laundry). You have 3 minutes to brainstorm and assign roles. Go!",
        "teacherTalkVi": "Teacher starts 3:00 timer and steps back to the rear of the room, giving full autonomy to groups.",
        "gestures": "Trigger the 3-minute countdown timer on screen, step back, quietly observing group dynamics.",
        "studentAction": "Students huddle in groups of 3, enthusiastically drafting speaking points with required chunks.",
        "boardSync": "Right Board: 'Family Chore Charter: Min 3 Chunks + Assigned Roles'.",
        "htmlContent": f"""
        <div class="slide-body-grid single-col" style="max-width: 1000px; margin: 0 auto; width: 100%;">
            <div class="mission-hero-card">
                <div class="mission-title">
                    <span>🏆</span> COMMUNICATIVE MISSION: 1-MINUTE FAMILY CHORE CHARTER
                </div>
                <p style="font-size: 15px; color: #cbd5e1; line-height: 1.5;">
                    In groups of 3, design an equitable, realistic Family Chore Charter for a contemporary family to present orally in 60 seconds.
                </p>

                <ul class="mission-criteria-list">
                    <li>
                        <span class="badge">CRITERION 1</span>
                        <span>Incorporate at least <strong>3 Target Chunks</strong>: <em>breadwinner, share housework, heavy lifting, do the cooking, laundry</em>.</span>
                    </li>
                    <li>
                        <span class="badge">CRITERION 2</span>
                        <span>Ensure a fair, practical division of duties based on schedule, health, and capability.</span>
                    </li>
                    <li>
                        <span class="badge">CRITERION 3</span>
                        <span>100% spoken participation: each member must deliver at least 2 complete spoken sentences.</span>
                    </li>
                </ul>

                <div class="timer-widget" style="background: rgba(15, 23, 42, 0.9); padding: 12px 18px; border-radius: 8px;">
                    <div class="timer-display" style="font-size: 24px;">
                        <span>⏱ Group Planning Timer:</span>
                        <span class="slide-timer-text" style="color: #facc15; font-size: 28px;">03:00</span>
                    </div>
                    <div class="timer-btn-group">
                        <button class="timer-btn" onclick="startCurrentTimer()" style="padding: 7px 14px; font-size: 13px;">Start 3 Mins</button>
                        <button class="timer-btn" onclick="pauseCurrentTimer()" style="padding: 7px 14px; font-size: 13px;">Pause</button>
                        <button class="timer-btn" onclick="resetCurrentTimer()" style="padding: 7px 14px; font-size: 13px;">Reset</button>
                    </div>
                </div>
            </div>
        </div>
        """
    })

    # SLIDE 17: Wrap-up: Exit Ticket 3-2-1 Challenge
    slides.append({
        "id": 17,
        "title": "Formative Assessment: Exit Ticket 3-2-1",
        "stage": "Stage 5: Wrap-up & Assessment (00:54 - 00:58)",
        "type": "exit-ticket",
        "maxSteps": 1,
        "timerSeconds": 180,
        "teacherTalkEn": "Pens in hand! Look at your Exit Ticket slips. You have 3 minutes of absolute silence to complete the 3-2-1 Challenge: 3 collocations you remember best today, 2 true sentences about your life, and 1 spelling or pronunciation trap you must avoid. No books, no chatting. Pure active recall. Go!",
        "teacherTalkVi": "Teacher collects slips quietly while observing silent retrieval reflection.",
        "gestures": "Distribute slips, stand attentively monitoring silent active recall.",
        "studentAction": "100% of students work in complete silence, retrieving lexical items directly from memory into their slips.",
        "boardSync": "Right Board: 'Exit Ticket 3-2-1: 3 Chunks ➔ 2 Sentences ➔ 1 Trap'.",
        "htmlContent": f"""
        <div class="slide-body-grid single-col" style="max-width: 1050px; margin: 0 auto; width: 100%;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span style="font-size: 13.5px; color: #facc15; font-weight: 700; text-transform: uppercase;">
                    📝 FORMATIVE ASSESSMENT: EXIT TICKET 3-2-1 (SPACED ACTIVE RECALL)
                </span>
                <div class="timer-widget" style="margin: 0; padding: 3px 10px;">
                    <span class="slide-timer-text" style="font-family: var(--font-display); font-size: 16px; font-weight: 800; color: #facc15;">03:00</span>
                    <button class="timer-btn" onclick="startCurrentTimer()" style="margin-left: 6px;">Start 3 Mins</button>
                </div>
            </div>

            <div class="exit-ticket-grid">
                <div class="exit-box b1">
                    <h4><span>3️⃣</span> CHUNKS</h4>
                    <p>Write down <strong>3 collocations / chunks</strong> you remember most deeply and can pronounce with full confidence today.</p>
                    <div style="margin-top: auto; border-top: 1px dashed #334155; padding-top: 6px; font-size: 11.5px; color: #64748b;">
                        Example: <em>primary breadwinner, do the laundry...</em>
                    </div>
                </div>

                <div class="exit-box b2">
                    <h4><span>2️⃣</span> SENTENCES</h4>
                    <p>Write <strong>2 complete sentences</strong> reflecting true facts about your own family using 2 of the chunks above.</p>
                    <div style="margin-top: auto; border-top: 1px dashed #334155; padding-top: 6px; font-size: 11.5px; color: #64748b;">
                        Example: <em>In my family, my dad does the cooking...</em>
                    </div>
                </div>

                <div class="exit-box b3">
                    <h4><span>1️⃣</span> TRAP</h4>
                    <p>Identify <strong>1 spelling trap</strong> (double consonants / silent letters) or pronunciation nuance to remember.</p>
                    <div style="margin-top: auto; border-top: 1px dashed #334155; padding-top: 6px; font-size: 11.5px; color: #64748b;">
                        Example: <em>breadwinner (double n, /e/ with ea)...</em>
                    </div>
                </div>
            </div>

            <div style="margin-top: 12px; background: rgba(15, 23, 42, 0.8); border: 1px solid var(--border); border-radius: 8px; padding: 8px 14px; text-align: center; color: #94a3b8; font-size: 13px;">
                ⚡ <strong>Core Rule:</strong> Closed-book retrieval • Drawing directly from long-term memory (defeating Ebbinghaus curve).
            </div>
        </div>
        """
    })

    # SLIDE 18: Delayed Feedback & Spaced Retrieval Contract
    slides.append({
        "id": 18,
        "title": "Delayed Feedback & Spaced Contract",
        "stage": "Stage 5: Wrap-up & Assessment (00:58 - 01:00)",
        "type": "delayed-feedback",
        "maxSteps": 1,
        "timerSeconds": 60,
        "teacherTalkEn": "Stop writing. Pass your slips to the aisle right now. While I collect them, look at the Left Board! During our fluency pitch, I noticed two tiny slips: someone said 'do a decision' and wrote 'breadwiner with one n'. Let's correct it together: MAKE a decision, and DOUBLE 'N' in breadwinner! Great job catching that!",
        "teacherTalkVi": "Teacher collects tickets, delivers delayed corrective feedback praising communication effort first, establishes Pimsleur schedule.",
        "gestures": "Collect Exit Tickets, tap Left Board with red marker, smile warmly encouraging the whole class.",
        "studentAction": "Students hand in tickets, pack materials, and chorally respond: 'Thank you and goodbye, teacher!'",
        "boardSync": "Left Board: 'MAKE a decision ✔ • BREADWINNER ✔'. Right Board: 'Pimsleur: 24h cards.html & 7d index.html'.",
        "htmlContent": f"""
        <div class="slide-body-grid" style="grid-template-columns: 1fr 1fr; gap: 20px; align-items: center;">
            <div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 20px; display: flex; flex-direction: column; gap: 12px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 18px;">🔍</span>
                    <h3 style="font-family: var(--font-display); font-size: 16px; font-weight: 800; color: #facc15;">
                        DELAYED ERROR FEEDBACK (SLIP CORRECTION)
                    </h3>
                </div>

                <div style="background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.35); border-radius: 8px; padding: 10px 14px;">
                    <span style="color: #fca5a5; font-size: 12.5px; text-decoration: line-through;">✘ do a decision</span>
                    <div style="color: #6ee7b7; font-weight: 700; font-size: 15px; margin-top: 3px;">
                        ➔ ✔ MAKE a decision
                    </div>
                </div>

                <div style="background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.35); border-radius: 8px; padding: 10px 14px;">
                    <span style="color: #fca5a5; font-size: 12.5px; text-decoration: line-through;">✘ breadwiner (one 'n')</span>
                    <div style="color: #6ee7b7; font-weight: 700; font-size: 15px; margin-top: 3px;">
                        ➔ ✔ BREADWINNER (double 'nn')
                    </div>
                </div>

                <div style="font-size: 12.5px; color: #94a3b8; font-style: italic;">
                    *Praise first, correct after: Celebrate communicative fluency before addressing collocational accuracy.*
                </div>
            </div>

            <div style="background: linear-gradient(135deg, #1e3a8a, #0f172a); border: 2px solid #3b82f6; border-radius: 12px; padding: 20px; display: flex; flex-direction: column; gap: 14px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 18px;">📜</span>
                    <h3 style="font-family: var(--font-display); font-size: 16px; font-weight: 800; color: #38bdf8;">
                        SPACED RETRIEVAL CONTRACT (PIMSLEUR)
                    </h3>
                </div>

                <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid var(--border); border-radius: 8px; padding: 12px;">
                    <span style="color: #facc15; font-weight: 800; font-size: 12px; text-transform: uppercase;">Milestone 1: After 24 Hours</span>
                    <p style="color: #ffffff; font-size: 13px; margin-top: 3px;">
                        Open <code>cards.html</code> (meanings hidden). Inspect visual cues and listen to native audio to actively recall spelling and stress beats.
                    </p>
                </div>

                <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid var(--border); border-radius: 8px; padding: 12px;">
                    <span style="color: #10b981; font-weight: 800; font-size: 12px; text-transform: uppercase;">Milestone 2: After 7 Days</span>
                    <p style="color: #ffffff; font-size: 13px; margin-top: 3px;">
                        Access <code>index.html</code> (Practice Mode) to complete 10 randomised contextual questions, cementing chunks into permanent memory.
                    </p>
                </div>
            </div>
        </div>
        """
    })

    return slides

def render_slides_html(unit_dir, unit_id, slides):
    """Generates the slides.html file string"""
    slides_html_content = ""
    overview_cards_html = ""

    for idx, s in enumerate(slides):
        active_class = " active-slide" if idx == 0 else ""
        slides_html_content += f"""
        <section class="slide-canvas{active_class}" id="slide-{idx}" data-slide-index="{idx}">
            <div class="slide-top-header">
                <div class="slide-title-wrap">
                    <h2>
                        <span>{s['title']}</span>
                    </h2>
                    <div class="slide-subtitle">{s['stage']}</div>
                </div>
                <div class="slide-meta-pills">
                    <span class="time-badge">⏱ {s['timerSeconds']}s</span>
                    <span class="involvement-badge">{s['type'].upper()}</span>
                </div>
            </div>
            {s['htmlContent']}
        </section>
        """

        overview_cards_html += f"""
        <div class="overview-card" onclick="jumpToSlide({idx})">
            <div class="ov-num">SLIDE {idx + 1} • {s['stage'].split('(')[0].strip()}</div>
            <div class="ov-title">{s['title']}</div>
            <div class="ov-stage">Builds: {s['maxSteps']} | Duration: {s['timerSeconds']}s</div>
        </div>
        """

    clean_slides_json = []
    for s in slides:
        clean_slides_json.append({
            "id": s["id"],
            "title": s["title"],
            "stage": s["stage"],
            "type": s["type"],
            "maxSteps": s["maxSteps"],
            "timerSeconds": s["timerSeconds"],
            "teacherTalkEn": s["teacherTalkEn"],
            "teacherTalkVi": s["teacherTalkVi"],
            "gestures": s["gestures"],
            "studentAction": s["studentAction"],
            "boardSync": s["boardSync"]
        })

    rendered_html = SLIDES_HTML_TEMPLATE.format(
        deck_title=f"Unit {unit_id.replace('unit-', '').upper()} - 60-Minute Interactive Slide Deck",
        unit_badge=f"GS10 {unit_id.upper()}",
        total_slides=len(slides),
        slides_html_content=slides_html_content,
        overview_cards_html=overview_cards_html,
        slides_json_data=json.dumps(clean_slides_json, ensure_ascii=False)
    )

    return rendered_html

def render_slides_markdown(unit_id, slides):
    """Generates the slides.md detailed specification file in 100% English"""
    md = f"""# DETAILED CLASSROOM SLIDE SCRIPT (SLIDES.MD): {unit_id.upper()}
> **Professional Classroom Slide Presentation System:** Slide-by-slide visual layout, progressive clicker builds, exact images, Concept Checking Questions (CCQs), and verbatim Teacher Teleprompter.
> **Pedagogical Foundations:** Paul Nation (Four Strands), Michael Lewis (Lexical Approach), Laufer & Hulstijn (Task Involvement Load = 5).

- **Lesson Scope:** 18 Standard Slides (Mapping directly to the 5 stages of the 60-minute lesson delivery)
- **Interactive Delivery App:** `slides.html` (Runs offline in any web browser; supports presenter clicker, timers, and shortcuts `P`, `F`, `B`, `T`, `O`)
- **Visual Assets:** `lessons/media/gs10/{unit_id}/images/`
- **Audio Assets:** `lessons/media/gs10/{unit_id}/audio/`

---

"""
    for idx, s in enumerate(slides):
        md += f"""## SLIDE {idx + 1:02d}: {s['title'].upper()}
- **Duration:** {s['timerSeconds']} seconds | **Stage:** {s['stage']}
- **Slide Type:** `{s['type']}` | **Max Clicker Builds:** {s['maxSteps']} steps

### 1. PROJECTOR DISPLAY SPECIFICATIONS
"""
        if s.get("imagePath"):
            md += f"""- **Visual Asset (Image):**
  - **File Path:** `{s['imagePath']}`
  - **Visual Content & Prompt Context:** *"{s.get('imageDesc', '')}"*
"""

        if s.get("ccqsList"):
            md += "- **Concept Checking Questions (CCQs) Projected on Screen:**\n"
            for q_idx, c in enumerate(s["ccqsList"]):
                md += f"  - **CCQ {q_idx + 1}:** *\"{c['q']}\"*\n"
                md += f"    - **Answer Key (Revealed on Teacher Click):** `✔ {c['a']}`\n"

        if s.get("phonetics"):
            md += f"""- **Spoken Form & Phonology:**
  - International Phonetic Alphabet (IPA): `{s['phonetics']['ipa']}` (UK) | Beat: **{s['phonetics']['beat']}**
  - Native Audio File: `{s['phonetics']['audio']}`
  - Mumble Drill: 3-second animated silent articulation countdown before choral drill.
"""

        if s.get("spellingTrap"):
            md += f"""- **Written Form & Spelling Traps:**
  - Displayed Word: **{s['spellingTrap']['word']}**
  - Alert: *{s['spellingTrap']['alert']}*
"""

        if s.get("collocationInfo"):
            md += f"""- **Collocation Grid & Personalised Sentence Frame:**
  - Collocation Grid 5-5-1: `[{', '.join(s['collocationInfo']['collocs'])}] + {s['collocationInfo']['center']}`
  - Semi-fixed Sentence Frame: *"{s['collocationInfo']['frame']}"*
  - Personalisation Countdown: **60 seconds**
"""

        if s['type'] == 'odd-one-out':
            md += """- **15-Second Mini-Whiteboard Challenge (Odd-One-Out Collocation Blitz):**
  - Row 1 (DO): *housework, household chores, the cooking, [a decision]* ➔ Impostor: **a decision** (MAKE a decision)
  - Row 2 (SHARE): *housework, responsibility, thoughts, [a heavy lifting]* ➔ Impostor: **a heavy lifting** (DO the heavy lifting)
  - Row 3 (MAKE): *breakfast, an effort, a choice, [the laundry]* ➔ Impostor: **the laundry** (DO the laundry)
  - **Teacher Action:** Initially, all options appear neutral. Students write on mini-whiteboards during the 15s timer. The teacher clicks to unveil each impostor one row at a time.
"""
        elif s['type'] == 'thematic-hook':
            md += """- **Visual Thematic Hook & Contrast:**
  - **Photo A (`breadwinner.webp`):** Working father returning home late with a heavy briefcase, bearing the solitary financial burden.
  - **Photo B (`housework.webp`):** Family members happily sharing chores and bonding in the kitchen.
  - **Cognitive Priming Question:** *"Which life looks happier, and who carries the heavier load?"*
"""
        elif s['type'] == 'practice-clues':
            md += """- **Speed Collocation & Clue Underlining (Think-Pair-Share):**
  - Question 1: *support our entire family* ➔ **breadwinner**
  - Question 2: *rearranging heavy oak cupboards* ➔ **heavy lifting**
  - Question 3: *after having dinner together* ➔ **washing-up**
  - Question 4: *equally [ ? ] the household chores* ➔ **share**
  - **Teacher Action:** Questions initially display clean. Teacher triggers partner clue highlighting, then reveals correct answers.
"""
        elif s['type'] == 'practice-matrix':
            md += """- **Word Family Morphology Matrix:**
  - Root SUPPORT: Verb `support` ➔ Noun `supporter / support` ➔ Adj `supportive`
  - Root RESPONSIBLE: Verb `take responsibility` ➔ Noun `responsibility` ➔ Adj `responsible`
  - Root DIVIDE: Verb `divide / split` ➔ Noun `division` ➔ Adj `divisible`
  - **Teacher Action:** Cells are initially masked with `[ Click to Reveal ]`. Teacher unmasks answers after student notebook work.
"""
        elif s['type'] == 'cascade-dialogue':
            md += """- **Cascade 3-Part Exchange Dialogue Scaffold:**
  - **Turn 1 (Partner A - Problem Initiator):** *"The living room is completely cluttered, and I still have to do the laundry before 6 P.M.!"*
  - **Turn 2 (Partner B - I-Focus Solution):** *"Don't worry, Mom! I'll take care of the living room and do the heavy lifting right now."*
  - **Turn 3 (Partner A - You-Focus Follow-up):** *"Thanks a million! Could you also help me do the washing-up after dinner tonight?"*
"""
        elif s['type'] == 'communicative-task':
            md += """- **Communicative Mission: 1-Minute Family Chore Charter:**
  - 3 minutes of group planning (3:00 countdown timer).
  - Conditions: Use at least 3 Target Chunks (*breadwinner, share housework, heavy lifting, do the cooking, laundry*).
"""
        elif s['type'] == 'exit-ticket':
            md += """- **Formative Assessment: Exit Ticket 3-2-1 Challenge:**
  - **3 Chunks:** 3 collocations remembered most deeply.
  - **2 Sentences:** 2 true sentences reflecting family reality.
  - **1 Trap:** 1 spelling or pronunciation trap to avoid.
  - Silent reflection timer: **3 minutes**.
"""
        elif s['type'] == 'delayed-feedback':
            md += """- **Delayed Corrective Feedback & Spaced Retrieval Contract:**
  - Slip corrections: *do a decision* ➔ `MAKE a decision` | *breadwiner* ➔ `BREADWINNER (double 'nn')`.
  - Pimsleur schedule: 24 hours on `cards.html` (meanings hidden); 7 days on `index.html` (practice test).
"""

        md += f"""
### 2. TEACHER PRESENTER TELEPROMPTER & DELIVERY SCRIPT
- **Verbatim Teacher Talk:**
  > *"{s['teacherTalkEn']}"*
- **Physical Gestures & Stage Movement:** {s['gestures']}
- **Expected Student Actions:** {s['studentAction']}
- **3-Column Board Synchronization:** `{s['boardSync']}`

---

"""
    return md

def main():
    parser = argparse.ArgumentParser(description="Generate Classroom Slide Deck Presentation")
    parser.add_argument("--unit", default="unit-1", help="Unit name, e.g. unit-1")
    parser.add_argument("--workspace", default="d:/GS10", help="Root workspace directory")
    args = parser.parse_args()

    workspace_dir = Path(args.workspace)
    unit_dir = workspace_dir / "lessons" / args.unit / "vocab"

    if not unit_dir.exists():
        print(f"Error: Unit directory does not exist: {unit_dir}")
        sys.exit(1)

    print(f"Generating slide deck for {args.unit} in {unit_dir}...")
    slides = generate_slides_data(unit_dir, args.unit)

    # 1. Output slides.html
    html_output_path = unit_dir / "slides.html"
    rendered_html = render_slides_html(unit_dir, args.unit, slides)
    with open(html_output_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)
    print(f"Created: {html_output_path} ({len(rendered_html)} bytes)")

    # 2. Output slides.md
    md_output_path = unit_dir / "slides.md"
    rendered_md = render_slides_markdown(args.unit, slides)
    with open(md_output_path, "w", encoding="utf-8") as f:
        f.write(rendered_md)
    print(f"Created: {md_output_path} ({len(rendered_md)} bytes)")

    print(f"Successfully generated 18 slides for {args.unit}!")

if __name__ == "__main__":
    main()
