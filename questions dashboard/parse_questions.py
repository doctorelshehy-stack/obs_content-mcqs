#!/usr/bin/env python3
"""
Parse all question Markdown files and generate a JSON data bundle
for the interactive dashboard.
"""

import re
import json
import os

BASE_DIR = "/media/mohamed/projects4/projects/obstaric/obs app/questions dashboard"

FILES = {
    "exams": {
        "questions": "Exams Qs - MCQs Only.md",
        "answers": "Exams Qs - MCQs Only - ANSWER KEY.md"
    },
    "quizzes": {
        "questions": "Quizzes Qs - MCQs Only.md",
        "answers": "Quizzes Qs - MCQs Only - ANSWER KEY.md"
    },
    "other": {
        "questions": "Other Qs - MCQs Only.md",
        "answers": "Other Qs - MCQs Only - ANSWER KEY.md"
    },
    "final_41": {
        "questions": "final_41_questions.md",
        "answers": "final_41_questions - ANSWER KEY.md"
    }
}


def extract_mcq_questions(text, source_name):
    """Extract MCQ questions from MCQs-only format like Exams/Quizzes/Other."""
    questions = []
    blocks = re.split(r'^## Question (\d+)', text, flags=re.MULTILINE)
    if blocks and not blocks[0].startswith('##'):
        blocks = blocks[1:]

    current_num = None
    current_block = ""

    for i, block in enumerate(blocks):
        block = block.strip()
        if i % 2 == 0:
            current_num = block
        else:
            lines = block.split('\n')
            question_lines = []
            options = []
            in_options = False

            for line in lines:
                stripped = line.strip()
                if stripped.startswith('**Options:**') or stripped.startswith('*Options:*') or stripped == '**Options**' or stripped == 'Options:' or stripped.startswith('**Options :**'):
                    in_options = True
                    continue

                if in_options:
                    opt_match = re.match(r'^[\*\-\s]*\s*([a-eA-E])([\)\.])\s*(.*)', stripped)
                    if opt_match:
                        label = opt_match.group(1).lower()
                        option_text = opt_match.group(3).strip()
                        options.append({"label": label, "text": option_text})
                        continue
                    if not re.match(r'^[\*\-\s]*\s*[a-eA-E][\)\.]', stripped):
                        if stripped and not stripped.startswith('-') and not stripped.startswith('*'):
                            question_lines.append(stripped)
                else:
                    if stripped:
                        question_lines.append(stripped)

            question_text = ' '.join(question_lines).strip()

            if question_text:
                q_num = current_num if current_num else 0
                try:
                    q_num_int = int(q_num)
                except (ValueError, TypeError):
                    q_num_int = 0
                questions.append({
                    "id": f"{source_name}_q{q_num_int}",
                    "number": q_num_int,
                    "topic": source_name,
                    "question": question_text,
                    "options": options,
                    "answer": None,
                    "answerText": None,
                    "justification": None,
                    "type": "mcq"
                })

    return questions


def extract_final_41_questions(text, source_name):
    """Extract questions from final_41_questions.md which has mixed formats."""
    questions = []
    q_counter = 0

    # Extract MCQs from the MCQ section (Q9)
    mcq_section = re.search(r'### Q9\.\s*Multiple Choice Questions.*?(?=###|\Z)', text, re.DOTALL)
    if mcq_section:
        mcq_text = mcq_section.group()
        # Split on newline + optional spaces + digits + period + required space
        # Capture group (\d+) becomes odd indices in the result
        mcq_blocks = re.split(r'\n\s*(\d+)\.\s+', mcq_text)
        # re.split with capture group yields: [header, num1, content1, num2, content2, ...]
        # Skip index 0 (header) always; numbers at odd indices, content at even indices after the number

        for i in range(1, len(mcq_blocks), 2):
            if i + 1 >= len(mcq_blocks):
                break
            num_str = mcq_blocks[i].strip()
            content_block = mcq_blocks[i + 1]
            if not num_str or not content_block.strip():
                continue
            try:
                q_num = int(num_str)
            except ValueError:
                continue

            lines = content_block.split('\n')
            q_text_lines = []
            options = []
            for line in lines:
                stripped = line.strip()
                if not stripped:
                    continue
                # Match option patterns: - A) text, - A. text, A) text, A. text
                opt_match = re.match(r'^[\-\s]*([A-E])([\)\.])\s*(.*)', stripped)
                if opt_match:
                    label = opt_match.group(1).lower()
                    opt_text = opt_match.group(3).strip()
                    options.append({"label": label, "text": opt_text})
                else:
                    q_text_lines.append(stripped)

            if q_text_lines:
                q_counter += 1
                q_text = ' '.join(q_text_lines).strip()
                questions.append({
                    "id": f"{source_name}_mcq{q_counter}",
                    "number": q_counter,
                    "topic": source_name,
                    "section": "MCQs (Q9)",
                    "question": q_text,
                    "options": options,
                    "answer": None,
                    "answerText": None,
                    "justification": None,
                    "type": "mcq"
                })

    # Extract essay questions
    essay_section = re.search(r'## I\)\s*Short Essay Questions.*?(?=## II\)|\Z)', text, re.DOTALL)
    if essay_section:
        essay_text = essay_section.group()
        essay_qs = re.findall(r'(Q\d+)[-–]\s*(.*?)(?=Q\d+[-–]|\Z)', essay_text, re.DOTALL)
        for eq_num, eq_text in essay_qs:
            q_counter += 1
            eq_text_clean = eq_text.strip().strip()
            questions.append({
                "id": f"{source_name}_essay{q_counter}",
                "number": q_counter,
                "topic": source_name,
                "section": f"Short Essay ({eq_num})",
                "question": eq_text_clean,
                "options": [],
                "answer": None,
                "answerText": None,
                "justification": None,
                "type": "essay"
            })

    # Extract problem solving questions
    pbl_section = re.search(r'## II\)\s*Problem Solving Questions.*?(?=### Q8|\Z)', text, re.DOTALL)
    if pbl_section:
        pbl_text = pbl_section.group()
        pbl_qs = re.findall(r'(Q\d+)[-–]\s*(.*?)(?=Q\d+[-–]|\Z)', pbl_text, re.DOTALL)
        for pq_num, pq_text in pbl_qs:
            q_counter += 1
            questions.append({
                "id": f"{source_name}_pbl{q_counter}",
                "number": q_counter,
                "topic": source_name,
                "section": f"Problem Solving ({pq_num})",
                "question": pq_text.strip().strip(),
                "options": [],
                "answer": None,
                "answerText": None,
                "justification": None,
                "type": "problem"
            })

    # Extract extended matching (Q8)
    em_section = re.search(r'### Q8\.\s*Extended Matching Questions.*?(?=### Q9|\Z)', text, re.DOTALL)
    if em_section:
        em_text = em_section.group()
        q_counter += 1
        questions.append({
            "id": f"{source_name}_match{q_counter}",
            "number": q_counter,
            "topic": source_name,
            "section": "Extended Matching (Q8)",
            "question": em_text.strip(),
            "options": [],
            "answer": None,
            "answerText": None,
            "justification": None,
            "type": "matching"
        })

    # Extract family medicine questions
    fm_section = re.search(r'## III\)\s*Family Medicine Questions.*?(?=\Z)', text, re.DOTALL)
    if fm_section:
        fm_text = fm_section.group()
        fm_qs = re.findall(r'(Q\d+)[\.\s]\s*(.*?)(?=Q\d+[\.\s]|\Z)', fm_text, re.DOTALL)
        for fq_num, fq_text in fm_qs:
            q_counter += 1
            questions.append({
                "id": f"{source_name}_fm{q_counter}",
                "number": q_counter,
                "topic": source_name,
                "section": f"Family Medicine ({fq_num})",
                "question": fq_text.strip(),
                "options": [],
                "answer": None,
                "answerText": None,
                "justification": None,
                "type": "short_answer"
            })

    return questions


def parse_answer_key_mcq(text):
    """Parse the answer key for MCQ files (Exams, Quizzes format)."""
    answers = {}
    blocks = re.split(r'^## Question (\d+)', text, flags=re.MULTILINE)
    if blocks and not blocks[0].startswith('##'):
        blocks = blocks[1:]

    for i in range(0, len(blocks)-1, 2):
        num = blocks[i].strip()
        content = blocks[i+1]

        ans_match = re.search(r'\*\*\s*([a-eA-E])\s*[\)\.]\s', content)
        if not ans_match:
            ans_match = re.search(r'(?:Answer|answer)\s*[:：]\s*[\(\[]?([a-eA-E])', content)
        if not ans_match:
            ans_match = re.search(r'\*\*([a-eA-E])\*\*', content)

        just_match = re.search(r'(?:Justification|justification)\s*[:：]\s*(.*?)(?=\n\d|$)', content, re.DOTALL)
        bold_match = re.search(r'\*\*([^*]+)\*\*', content)

        answer_letter = ans_match.group(1).lower() if ans_match else None
        answer_text = bold_match.group(1) if bold_match else None
        justification = just_match.group(1).strip() if just_match else None

        answers[num] = {
            "answer": answer_letter,
            "answerText": answer_text,
            "justification": justification
        }

    return answers


def parse_final41_answer_key(text):
    """Parse the Final 41 answer key which uses a markdown TABLE for Q9 MCQs."""
    answers = {}

    # Extract the Q9 MCQ table — parses pipe-delimited markdown table rows
    table_section = re.search(r'### Q9\.\s*Multiple Choice Questions.*?(?=###|\Z)', text, re.DOTALL)
    if table_section:
        table_text = table_section.group()
        # Find rows with pipe separators
        rows = re.findall(r'^\|\s*(\d+)\s*\|.*?\|\s*\*\*([A-Ea-e])\s*[\)\.]\s*([^*]*?)\s*\*\*\s*\|.*?$', table_text, re.MULTILINE)
        for q_num, ans_letter, ans_full in rows:
            key = q_num  # string like "1", "2"
            # Extract justification from the rationale column — text after the last `|`
            row_pattern = re.compile(
                r'^\|\s*' + re.escape(q_num) + r'\s*\|'
                r'.*?\|\s*\*\*[^*]+\*\*\s*'  # skip to correct answer column
                r'\|\s*(.*?)\s*$',
                re.MULTILINE | re.DOTALL
            )
            justification = None
            full_row_match = row_pattern.search(table_text)
            if full_row_match:
                justification = full_row_match.group(1).strip()

            answers[key] = {
                "answer": ans_letter.lower(),
                "answerText": ans_full.strip(),
                "justification": justification
            }

    return answers


def parse_answer_key_other(text):
    """Parse 'Other Qs' answer key format: **Q1:** X) ..."""
    answers = {}
    lines = text.split('\n')
    current_q = None
    current_ans = None
    current_just = None

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        q_match = re.match(r'\*\*Q(\d+):\s*\*\*\s*', stripped)
        if q_match:
            if current_q:
                answers[current_q] = {
                    "answer": current_ans,
                    "answerText": None,
                    "justification": current_just
                }

            current_q = q_match.group(1)
            current_just = None

            after_label = stripped[q_match.end():]
            ans_letter_match = re.match(r'\(?([a-eA-E])([\)\.])\s', after_label)
            if ans_letter_match:
                current_ans = ans_letter_match.group(1).lower()
                current_just = after_label[ans_letter_match.end():]
            else:
                current_ans = None
                current_just = after_label
        elif current_q and stripped.startswith('*Justification'):
            current_just = stripped
        elif current_q and stripped.startswith('-') and '--' not in stripped:
            if current_just:
                current_just += ' ' + stripped

    if current_q:
        answers[current_q] = {
            "answer": current_ans,
            "answerText": None,
            "justification": current_just
        }

    return answers


def main():
    all_questions = []
    topic_info = {}

    for source_name, files in FILES.items():
        q_path = os.path.join(BASE_DIR, files["questions"])

        if not os.path.exists(q_path):
            print(f"Warning: {q_path} not found")
            continue

        with open(q_path, 'r', encoding='utf-8') as f:
            q_text = f.read()

        if source_name == "final_41":
            questions = extract_final_41_questions(q_text, source_name)
        else:
            questions = extract_mcq_questions(q_text, source_name)

        # Parse answer key
        answers = {}
        a_path = os.path.join(BASE_DIR, files["answers"])
        if os.path.exists(a_path):
            with open(a_path, 'r', encoding='utf-8') as f:
                a_text = f.read()
            if source_name == "other":
                answers = parse_answer_key_other(a_text)
            elif source_name == "final_41":
                answers = parse_final41_answer_key(a_text)
            else:
                answers = parse_answer_key_mcq(a_text)

        for q in questions:
            q_num = str(q["number"])
            if q_num in answers:
                q["answer"] = answers[q_num]["answer"]
                q["answerText"] = answers[q_num]["answerText"]
                q["justification"] = answers[q_num]["justification"]

        all_questions.extend(questions)
        mcq_count = sum(1 for q in questions if q["type"] == "mcq")
        topic_info[source_name] = {
            "label": source_name.replace('_', ' ').title(),
            "mcqCount": mcq_count,
            "totalCount": len(questions)
        }

    print(f"Exams: {sum(1 for q in all_questions if q['topic'] == 'exams')} questions")
    print(f"Quizzes: {sum(1 for q in all_questions if q['topic'] == 'quizzes')} questions")
    print(f"Other: {sum(1 for q in all_questions if q['topic'] == 'other')} questions")
    print(f"Final 41: {sum(1 for q in all_questions if q['topic'] == 'final_41')} questions")
    print(f"Total: {len(all_questions)} questions")
    print(f"Topics: {topic_info}")

    output = {
        "questions": all_questions,
        "topics": topic_info
    }

    output_path = os.path.join(BASE_DIR, "data", "questions-data.js")
    os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("// Auto-generated questions data bundle\n")
        f.write("// Generated by parse_questions.py\n")
        f.write("const QUESTIONS_DATA = ")
        f.write(json.dumps(output, ensure_ascii=False, indent=2))
        f.write(";\n")

    print(f"\nWritten to {output_path}")
    print(f"File size: {os.path.getsize(output_path):,} bytes")


if __name__ == "__main__":
    main()
