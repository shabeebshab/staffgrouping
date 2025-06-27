from django.shortcuts import render
from .forms import RawDataForm
import json
import re


def extract_data(raw_text):
    staff = []
    total_paid = 0.0
    lines = raw_text.strip().split('\n')

    i = 0
    while i < len(lines):
        if i + 2 >= len(lines):
            break

        name_line = lines[i].strip()
        name_parts = name_line.split()
        if len(name_parts) < 3:
            i += 1
            continue
        name = " ".join(name_parts[2:])

        paid_line = lines[i+2]
        paid_match = re.search(r'Paid:\s*₹?(\d+)', paid_line)
        category_match = re.search(r'Paid:\s*₹?\d+\s+([A-Za-z ]+?)\s+\d', paid_line)

        if paid_match:
            paid = float(paid_match.group(1))
            total_paid += paid
        else:
            paid = 0.0

        

        category = category_match.group(1).strip() if category_match else "Unknown"

        staff.append({
            'name': name,
            'paid': paid,
            'category': category
        })

        i += 3

    return staff, total_paid

def paste_view(request):
    if request.method == 'POST':
        form = RawDataForm(request.POST)
        if form.is_valid():
            raw = form.cleaned_data['raw_data']
            staff, total_paid = extract_data(raw)
            request.session['staff_data'] = json.dumps(staff)  # convert to JSON string
            request.session['total_paid'] = total_paid
            return render(request, 'preview.html', {
                'staff': staff,
                'total_paid': total_paid
            })
    else:
        form = RawDataForm()
    return render(request, 'paste.html', {'form': form})

def group_view(request):
    import json
    staff = json.loads(request.session.get('staff_data', '[]'))
    group_size = int(request.GET.get('size', 10))

    # Split staff into main and others
    main_boys = [s for s in staff if 'main' in s['category'].lower()]
    others = [s for s in staff if 'main' not in s['category'].lower()]

    total_groups = max(1, (len(staff) + group_size - 1) // group_size)
    groups = [[] for _ in range(total_groups)]

    # Distribute staff members fairly into groups
    for idx, person in enumerate(main_boys + others):
        groups[idx % total_groups].append(person)

    # Add total paid per group
    for group in groups:
        group_total = sum(float(p['paid']) for p in group)
        for member in group:
            member['group_total'] = group_total

    # Choose template based on URL parameter
    template = 'print.html' if request.GET.get('print') == '1' else 'groups.html'
    return render(request, template, {'groups': groups})



