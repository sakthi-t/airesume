# utils/data_models.py
from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime
from utils.date_utils import parse_date


class Entry(BaseModel):
    title: str
    org: Optional[str] = None
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    remarks: Optional[str] = None


def _get_list(form: Any, key: str) -> List[str]:
    """
    Helper to pull lists from Flask request.form (has getlist)
    or from a dict-of-lists (like request.form.to_dict(flat=False)).
    """
    if hasattr(form, "getlist"):
        return form.getlist(key)
    val = form.get(key, [])
    if isinstance(val, list):
        return val
    if val is None:
        return []
    # single string -> return as single-element list
    return [val]


def _get_first(form: Any, key: str) -> str:
    lst = _get_list(form, key)
    return lst[0] if lst else ""


def normalize_form(form: Any) -> dict:
    """
    Convert submitted form (Flask request.form or dict-of-lists)
    into a normalized resume dict:
      {
        "basics": { ... },
        "experience": [Entry, ...],
        "projects": [Entry, ...],
        "education": [Entry, ...],
        "skills": [...],
        "awards": [...]
      }
    """
    # Basics
    basics = {
        "name": _get_first(form, "name"),
        "email": _get_first(form, "email"),
        "phone": _get_first(form, "phone"),
        "website": _get_first(form, "website"),
        "linkedin": _get_first(form, "linkedin"),
        "github": _get_first(form, "github"),
        "summary": _get_first(form, "summary"),
    }

    # Experience
    experience = []
    exp_titles = _get_list(form, "exp_title")
    exp_orgs = _get_list(form, "exp_org")
    exp_starts = _get_list(form, "exp_start")
    exp_ends = _get_list(form, "exp_end")
    exp_remarks = _get_list(form, "exp_remarks")
    max_exp = max(len(exp_titles), len(exp_orgs), len(exp_starts), len(exp_ends), len(exp_remarks))
    for i in range(max_exp):
        title = exp_titles[i] if i < len(exp_titles) else ""
        org = exp_orgs[i] if i < len(exp_orgs) else ""
        start = parse_date(exp_starts[i]) if i < len(exp_starts) else None
        end = parse_date(exp_ends[i]) if i < len(exp_ends) else None
        remarks = exp_remarks[i] if i < len(exp_remarks) else ""
        # only add if there's content
        if title.strip() or org.strip() or remarks.strip():
            experience.append(Entry(title=title, org=org, start=start, end=end, remarks=remarks))

    # Projects
    projects = []
    proj_titles = _get_list(form, "proj_title")
    proj_orgs = _get_list(form, "proj_org")
    proj_starts = _get_list(form, "proj_start")
    proj_ends = _get_list(form, "proj_end")
    proj_remarks = _get_list(form, "proj_remarks")
    max_proj = max(len(proj_titles), len(proj_orgs), len(proj_starts), len(proj_ends), len(proj_remarks))
    for i in range(max_proj):
        title = proj_titles[i] if i < len(proj_titles) else ""
        org = proj_orgs[i] if i < len(proj_orgs) else ""
        start = parse_date(proj_starts[i]) if i < len(proj_starts) else None
        end = parse_date(proj_ends[i]) if i < len(proj_ends) else None
        remarks = proj_remarks[i] if i < len(proj_remarks) else ""
        if title.strip() or org.strip() or remarks.strip():
            projects.append(Entry(title=title, org=org, start=start, end=end, remarks=remarks))

    # Education
    education = []
    edu_titles = _get_list(form, "edu_title")
    edu_orgs = _get_list(form, "edu_org")
    edu_starts = _get_list(form, "edu_start")
    edu_ends = _get_list(form, "edu_end")
    edu_remarks = _get_list(form, "edu_remarks")
    max_edu = max(len(edu_titles), len(edu_orgs), len(edu_starts), len(edu_ends), len(edu_remarks))
    for i in range(max_edu):
        title = edu_titles[i] if i < len(edu_titles) else ""
        org = edu_orgs[i] if i < len(edu_orgs) else ""
        start = parse_date(edu_starts[i]) if i < len(edu_starts) else None
        end = parse_date(edu_ends[i]) if i < len(edu_ends) else None
        remarks = edu_remarks[i] if i < len(edu_remarks) else ""
        if title.strip() or org.strip() or remarks.strip():
            education.append(Entry(title=title, org=org, start=start, end=end, remarks=remarks))

    # Skills: support either a single textarea (comma-separated) or multiple inputs
    skills_raw = _get_list(form, "skills")
    if len(skills_raw) == 1:
        # split comma separated
        skills = [s.strip() for s in skills_raw[0].split(",") if s.strip()]
    else:
        skills = [s.strip() for s in skills_raw if s.strip()]

    # Awards: support single textarea (newline separated) or multiple inputs
    awards_raw = _get_list(form, "awards")
    if len(awards_raw) == 1:
        awards = [a.strip() for a in awards_raw[0].split("\n") if a.strip()]
    else:
        awards = [a.strip() for a in awards_raw if a.strip()]

    return {
        "basics": basics,
        "experience": experience,
        "projects": projects,
        "education": education,
        "skills": skills,
        "awards": awards,
    }
