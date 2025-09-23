from django.db import models


class Information(models.Model):
    SEX = (
        ("Nam", "Nam"),
        ("Nữ", "Nữ"),
    )
    QUAN_HE_VOI_CHU_HO = (
        ("Chủ hộ", "Chủ hộ"),
        ("Chồng", "Chồng"),
        ("Vợ", "Vợ"), 
        ("Con", "Con"),
        ("Cháu", "Cháu"),
        ("Con dâu", "Con dâu"), 
        ("Con rễ", "Con rễ"),
    )
    BAC_TOT_NGHIEP = (
        ("MN", "MN"),
        ("TH", "TH"),
        ("THCS", "THCS"),
        ("THPT", "THPT"),
        ("ĐH", "ĐH"), 
    )

    name = models.CharField(max_length=120)
    day_bir = models.IntegerField(blank=True, null=True)
    month_bir = models.IntegerField(blank=True, null=True)
    year_bir = models.IntegerField()
    sex = models.CharField(max_length=120, default="Nam", choices=SEX)
    dan_toc = models.CharField(max_length=120, default="Kinh")
    address = models.TextField(default="Tổ 11 - Đông An")
    so_phieu = models.TextField(default="DA11001")
    dien_cu_tru = models.TextField(default="Thường trú")
    lop_hoc = models.TextField(blank=True, default="")
    truong = models.TextField(default=" ", blank=True, null=True)
    bac_tot_nghiep = models.TextField(choices=BAC_TOT_NGHIEP, blank=True, null=True)
    nam_tot_nghiep = models.IntegerField(blank=True, null=True)
    quan_he_voi_chu_ho = models.TextField(choices=QUAN_HE_VOI_CHU_HO)
    ten_cha_hoac_me = models.TextField(blank=True, default="")
    sdt = models.TextField(blank=True, default="")
    note = models.TextField(blank=True, default="")

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["id"]