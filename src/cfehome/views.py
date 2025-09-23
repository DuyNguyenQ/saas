from django.shortcuts import render
from visits.models import PageVisit
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from infor.models import Information

LOGIN_URL = settings.LOGIN_URL

import openpyxl
from django.http import HttpResponse
from infor.models import Information
from openpyxl.styles import PatternFill, Font, Alignment

def export_information_excel(request):
    # Tạo workbook và worksheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Information"
    white_font_bold = Font(color="ffffff", size=11, bold=True)
    center_alignment = Alignment(horizontal='center', vertical='center')
    # Thêm dòng header mới với merge cells
    # ws.append(["Thông tin đối tượng", "", "", "", "", "", "", "", "", "", 
    #            "Thông tin nơi đang ở", "", "", "", "", "",
    #            "Thông tin học tập", "", "", "", "", "", "","", "", "", "", "", "", "","",
    #            "Xóa mù chữ", "", "",
    #            "Khuyết tật", "", "", "", "", "", "", "", "", "abc", "",
    #           ])
    
    # # Merge các ô cho dòng header mới
    # ws.merge_cells('A1:J1')  # Merge 10 ô đầu
    # ws.merge_cells('K1:P1')  # Merge 5 ô tiếp theo
    # ws.merge_cells('Q1:AE1')  # Merge 20 ô cuối
    # ws.merge_cells('AF1:AH1')
    # ws.merge_cells('AI1:AR1')
    # ws.merge_cells('AS1:AU1')
    # ws.merge_cells('AU1:AX1')

    for cell in ws[1]:  # Từ cột A đến O (15 cột)
        # cell = ws.cell(row=1, column=col)
        # cell.fill = blue_fill
        # cell.font = white_font_bold
        cell.alignment = center_alignment

    line_2 = [
        "TT", "Họ đệm", "Tên", "Ngày", "Tháng", "Năm sinh", "Nữ", "Dân tộc", "Tôn giáo",
        "Diện ưu tiên", "Họ đệm", "Tên",  "Địa chỉ: số nhà, tên đường, tổ (nếu có)",
        "Số phiếu", "Diện cư trú", "Tình trạng cư trú", "Khối học", "Lớp học", "", "",
        "Mã trường", "Bậc tốt nghiệp", "Bổ túc", "Năm tốt nghiệp", "Bậc TN nghề", "",
        "Năm TN nghề", "Lớp", "Năm", "Lớp", "Năm", "Đang học lớp", "Hoàn thành lớp",
        "Tái mù chữ mức", "Khuyết tật vận động", "Khuyết tật nghe nói", "Khuyết tật nhìn",
        "Khuyết tật thần kinh, tâm thần", "Khuyết tật trí tuệ", "Khuyết tật học tập",
        "Tự kỷ", "Khuyết tật khác", "Có chứng nhận khuyết tật", "Khả năng học tập",
        "Hoàn cảnh đặc biệt", "Chi tiết hoàn cảnh đặt biệt", "Quan hệ với chủ hộ", 
        "Họ tên cha hoặc mẹ", "Điện thoại", "Ghi chú",
    ]
    ws.append(line_2)
    line_3 = [x for x in range(1,19)] + [""]*2 + [x for x in range(19, 24)] + [""] + [x for x in range(24, 48)]
    ws.append(line_3)

    red_fill = PatternFill(start_color="ff0000", end_color="ff0000", fill_type="solid")  # Mã màu xanh lá nhạt
    for cell in ws[2]:  
        cell.fill = red_fill
        cell.font = white_font_bold
        cell.alignment = center_alignment

    green_fill = PatternFill(start_color="33ff00", end_color="33ff00", fill_type="solid")  # Mã màu xanh lá nhạt
    for cell in ws[3]:  # Dòng thứ 2 (sau headers), openpyxl bắt đầu từ 1
        cell.fill = green_fill
        cell.font = white_font_bold
        cell.alignment = center_alignment
        

    # Lấy dữ liệu từ model
    row_index = 4
    for obj in Information.objects.all():
        name = obj.name.split()
        
        list_so_phieu = list(obj.so_phieu)
        tt = int("".join(list_so_phieu[2:]))%11000
        row = [
            tt if obj.quan_he_voi_chu_ho == "Chủ hộ" else " ",
            " ".join(name[0:-1]),
            name[-1],
            obj.day_bir,
            obj.month_bir,
            obj.year_bir,
            "x" if obj.sex == "Nữ" else "",
            obj.dan_toc,
            "","",
            " ".join(name[0:-1]),
            name[-1],
            obj.address,
            obj.so_phieu,
            obj.dien_cu_tru,
            "","",
            obj.lop_hoc,
            "", "",
            obj.truong,
            obj.bac_tot_nghiep,
            "",
            obj.nam_tot_nghiep,
            "","","","","","","","","","","","","","","","","","","","","","",
            obj.quan_he_voi_chu_ho,
            obj.ten_cha_hoac_me,
            obj.sdt,
            obj.note,
        ]
        ws.append(row)
        for cell in ws[row_index]:
            white_font_bold = Font(size=12)
            cell.alignment = center_alignment

        row_index += 1

    # Tạo response trả về file excel
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=information.xlsx'
    wb.save(response)
    return response

def home_page_view(request):
    html_template = "home.html"
    qs = PageVisit.objects.all()
    my_context = {
        "page_title": "Saas",
        "qs":  qs,
        "num_visit": qs.count(),
    }
    PageVisit.objects.create()
    return render(request, html_template, my_context)

VALID_CODE = "abc123"
@login_required(login_url=LOGIN_URL)
def pw_protect_view(request, *args, **kwargs):
    print(request.POST)
    is_allowed = request.session.get('protected_page_allowed', None)
    print(request.session.get('protected_page_allowed', None), type(request.session.get('protected_page_allowed', None)))
    if request.method == "POST":
        user_pw_sent = request.POST.get("code", None)
        if user_pw_sent==VALID_CODE:
            request.session["protected_page_allowed"] = True
    if is_allowed:
        return render(request, "home.html", {}) 
    return render(request, "protected/entry.html", {})


@login_required(login_url=LOGIN_URL)
def user_only_view(request, *args, **kwargs):
    return render(request, "protect/user_only_view.html", {})


@staff_member_required(login_url=LOGIN_URL)
def staff_only_view(request, *args, **kwargs):
    return render(request, "protect/staff_only_view.html", {})



