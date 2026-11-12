#!/usr/bin/env python3
"""Build the static portfolio from website-content.md. No third-party packages.

Usage:
    python build_site.py

Edit website-content.md, then run this script. The resulting index.html works
locally and on GitHub Pages. Changes to CSS/JS need no rebuild.
"""
from __future__ import annotations

from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'website-content.md'
TEMPLATE = ROOT / 'template.html'
OUTPUT = ROOT / 'index.html'


def parse_content(contents: str) -> dict[str, dict[str, str]]:
    sections: dict[str, dict[str, str]] = {}
    current_section = None
    current_field = None
    buffer: list[str] = []

    def flush():
        nonlocal buffer
        if current_section and current_field:
            sections[current_section][current_field] = '\n'.join(buffer).strip()
        buffer = []

    for line in contents.splitlines():
        if line.startswith('## '):
            flush()
            current_section = line[3:].strip().upper()
            sections[current_section] = {}
            current_field = None
        elif line.startswith('### '):
            flush()
            current_field = line[4:].strip().upper()
        elif current_section and current_field:
            buffer.append(line)
    flush()
    return sections


def safe(text: str) -> str:
    return escape(text, quote=True)


def inline(text: str) -> str:
    """Preserve authored line breaks, but never interpret arbitrary HTML."""
    return safe(text).replace('\n', '<br>')


def link(url: str, label: str, extra_class: str = '') -> str:
    if not url.startswith('https://'):
        return ''
    return (f'<a class="{extra_class}" href="{safe(url)}" target="_blank" '
            f'rel="noopener noreferrer">{safe(label)} <span aria-hidden="true">↗</span></a>')


def build(data: dict[str, dict[str, str]]) -> str:
    def v(group: str, field: str) -> str:
        return data[group][field]
    def t(group: str, field: str) -> str:
        return inline(v(group, field))

    journey = []
    for i in range(1, 5):
        group = f'JOURNEY_{i}'
        journey.append(f'''<article class="journey-item reveal">
          <div class="journey-index" aria-hidden="true">{t(group,'NUMBER')}</div>
          <div class="journey-copy"><p class="mini-label">{t(group,'LABEL')}</p>
          <h3>{t(group,'TITLE')}</h3><p>{t(group,'TEXT')}</p></div>
        </article>''')

    project_visuals = {
        'PROJECT_CONTEXT': '''<div class="project-art project-art-notes" aria-hidden="true">
          <div class="notes-panel"><div class="panel-top"><span class="panel-dot"></span><span class="panel-dot"></span><span class="panel-dot"></span><span class="panel-title">graph / before</span></div><div class="note-line">● &nbsp; Overview</div><div class="note-line">● &nbsp; Overview</div></div>
          <div class="notes-direction">→</div>
          <div class="notes-panel notes-panel-after"><div class="panel-top"><span class="panel-dot"></span><span class="panel-dot"></span><span class="panel-dot"></span><span class="panel-title">graph / after</span></div><div class="note-line">● &nbsp; Alpha – Overview</div><div class="note-line">● &nbsp; Beta – Overview</div></div>
        </div>''',
        'PROJECT_NOTIFIER': '''<div class="project-art project-art-notify" aria-hidden="true"><div class="notify-window"><div class="notify-icon">↗</div><div><small>AI Chat Notifications</small><strong>Your response is ready.</strong><span>Return to conversation</span></div><i class="notify-time">now</i></div><div class="quiet-text">STAY FOCUSED. WE'LL LET YOU KNOW.</div></div>''',
        'PROJECT_ZORO': '''<div class="project-art project-art-zoro" aria-hidden="true"><div class="zoro-head"><span class="live-dot"></span> ZORO / LOCAL ASSISTANT <span class="zoro-sep">●</span> IN DEVELOPMENT</div><div class="soundwave"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div><div class="zoro-flow"><span>Listen</span><b>→</b><span>Understand</span><b>→</b><span>Act</span></div></div>''',
        'PROJECT_SYNC': '''<div class="project-art project-art-sync" aria-hidden="true"><div class="sync-caption">REPOSITORY HEALTH</div><div class="sync-row"><span>main</span><span class="sync-good">● clean</span></div><div class="sync-row"><span>feature / local edits</span><span class="sync-hold">● hold</span></div><div class="sync-foot">Don't overwrite unfinished work.</div></div>'''
    }
    projects = []
    for key in ['PROJECT_CONTEXT', 'PROJECT_NOTIFIER', 'PROJECT_ZORO', 'PROJECT_SYNC']:
        kind = v(key, 'KIND').strip().lower()
        if kind not in ('published','development'):
            raise ValueError(f'{key}.KIND must be published or development')
        href = v(key,'LINK').strip()
        action = link(href,v(key,'LINK_LABEL'),'project-visit') if href else f'<span class="project-closed">{t(key,"LINK_LABEL")}</span>'
        visual = project_visuals[key]
        projects.append(f'''<article class="project-card project-{kind} reveal" data-kind="{kind}">
          <div class="project-meta"><span class="project-num">{t(key,'NUMBER')} / SELECTED WORK</span><span class="project-status">{t(key,'STATUS')}</span></div>
          {visual}
          <div class="project-body"><p class="project-type">{t(key,'SUBTITLE')}</p><h3>{t(key,'TITLE')}</h3>
          <p class="project-description">{t(key,'DESCRIPTION')}</p><p class="project-detail">{t(key,'DETAIL')}</p>
          <ul class="tech-tags">{''.join(f'<li>{safe(s.strip())}</li>' for s in v(key,'STACK').split(';') if s.strip())}</ul>
          <div class="project-footer">{action}</div></div>
        </article>''')

    skills = []
    for num,(prefix,number) in enumerate([('HARDWARE','01'),('SOFTWARE','02'),('AI','03'),('NETWORK','04')]):
        skills.append(f'''<article class="skill-row reveal"><span class="skill-number">{number}</span><h3>{t('SKILLS',prefix+'_TITLE')}</h3><p>{t('SKILLS',prefix+'_TEXT')}</p></article>''')

    certs = ''.join(f'<li>{t("CERTIFICATIONS",f"COMPLETED_{i}")}</li>' for i in range(1,5))
    hero_headline = v('HERO', 'HEADLINE').strip()
    # Splitting at first full stop is intentional for the editorial line treatment.
    first, sep, rest = hero_headline.partition('. ')
    if sep:
        first = first + '.'
    else:
        rest = ''
    hero_display = f'{safe(first)}' + (f'<span class="hero-second">{safe(rest)}</span>' if rest else '')

    replacements = {
        'SITE_NAME': t('SITE', 'NAME'),
        'SITE_LOCATION': t('SITE', 'LOCATION'),
        'SITE_SCHOOL': t('SITE', 'SCHOOL'),
        'SITE_CLASS_YEAR': t('SITE', 'CLASS_YEAR'),
        'SITE_EMAIL': safe(v('SITE', 'EMAIL')),
        'SITE_EMAIL_HREF': safe('mailto:'+v('SITE', 'EMAIL')),
        'SITE_GITHUB': safe(v('SITE', 'GITHUB')),
        'HERO_KICKER': t('HERO','KICKER'),
        'HERO_HEADLINE': hero_display,
        'HERO_INTRO': t('HERO','INTRO'),
        'HERO_CURRENT': t('HERO','CURRENT'),
        'HERO_NOTE': t('HERO','NOTE'),
        'ABOUT_EYEBROW': t('ABOUT','EYEBROW'),
        'ABOUT_TITLE': t('ABOUT','TITLE'),
        'ABOUT_PARAGRAPH_1': t('ABOUT','PARAGRAPH_1'),
        'ABOUT_PARAGRAPH_2': t('ABOUT','PARAGRAPH_2'),
        'ABOUT_QUOTE': t('ABOUT','QUOTE'),
        'JOURNEY_ITEMS': '\n'.join(journey),
        'PROJECTS_EYEBROW': t('PROJECTS','EYEBROW'),
        'PROJECTS_TITLE': t('PROJECTS','TITLE'),
        'PROJECTS_INTRO': t('PROJECTS','INTRO'),
        'PROJECT_CARDS': '\n'.join(projects),
        'SKILLS_EYEBROW': t('SKILLS','EYEBROW'),
        'SKILLS_TITLE': t('SKILLS','TITLE'),
        'SKILLS_INTRO': t('SKILLS','INTRO'),
        'SKILL_ROWS': '\n'.join(skills),
        'LEADERSHIP_EYEBROW': t('LEADERSHIP','EYEBROW'),
        'LEADERSHIP_TITLE': t('LEADERSHIP','TITLE'),
        'LEADERSHIP_STORY': t('LEADERSHIP','STORY'),
        'LEADERSHIP_FOLLOWUP': t('LEADERSHIP','FOLLOWUP'),
        'LEADERSHIP_VOLUNTEER': t('LEADERSHIP','VOLUNTEER'),
        'AWARDS_EYEBROW': t('AWARDS','EYEBROW'),
        'AWARDS_TITLE': t('AWARDS','TITLE'),
        'AWARD_1': t('AWARDS','AWARD_1'),
        'AWARD_1_META': t('AWARDS','AWARD_1_META'),
        'AWARD_2': t('AWARDS','AWARD_2'),
        'AWARD_2_META': t('AWARDS','AWARD_2_META'),
        'CERT_EYEBROW': t('CERTIFICATIONS','EYEBROW'),
        'CERT_TITLE': t('CERTIFICATIONS','TITLE'),
        'COMPLETED_CERTS': certs,
        'IN_PROGRESS_CERT': t('CERTIFICATIONS','IN_PROGRESS'),
        'GOALS_EYEBROW': t('GOALS','EYEBROW'),
        'GOALS_TITLE': t('GOALS','TITLE'),
        'GOALS_INTRO': t('GOALS','INTRO'),
        'GOALS_NOTE': t('GOALS','NOTE'),
        'RESUME_EYEBROW': t('RESUME','EYEBROW'),
        'RESUME_TITLE': t('RESUME','TITLE'),
        'RESUME_INTRO': t('RESUME','INTRO'),
        'RESUME_BUTTON': t('RESUME','BUTTON'),
        'CONTACT_EYEBROW': t('CONTACT','EYEBROW'),
        'CONTACT_TITLE': t('CONTACT','TITLE'),
        'CONTACT_INTRO': t('CONTACT','INTRO'),
        'CONTACT_EMAIL_BUTTON': t('CONTACT','EMAIL_BUTTON'),
        'CONTACT_GITHUB_BUTTON': t('CONTACT','GITHUB_BUTTON'),
    }

    output = TEMPLATE.read_text(encoding='utf-8')
    for key, value in replacements.items():
        output = output.replace('{{'+key+'}}',value)
    leftovers = re.findall(r'\{\{([A-Z_]+)\}\}',output)
    if leftovers:
        raise ValueError(f'Unresolved template fields: {sorted(set(leftovers))}')
    return output

if __name__ == '__main__':
    parsed = parse_content(SOURCE.read_text(encoding='utf-8'))
    OUTPUT.write_text(build(parsed), encoding='utf-8')
    print(f'Built {OUTPUT.name} from {SOURCE.name} ({OUTPUT.stat().st_size:,} bytes)')