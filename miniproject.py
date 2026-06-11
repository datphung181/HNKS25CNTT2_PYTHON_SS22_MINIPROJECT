import logging
"""
logging dùng để lưu lại hđ ghi làm vc vs file 

    logging.DEBUG
    logging.INFO / CHUONG TRINH HD BT
    logging.WARNING / CHUONG TRINH CANH BAO NHUNG VAN CHAY
    logging.ERROR / CHUONG TRINH BAO LOI 
    logging.CRITICAL / LOI CUC KI NGHIEM TRONG

CAC EXCEPTION HAY GẶP:
    valueerror: gia tri sai kieu  mong doi
    keyerror: truy cap key k ton tai
    indexerror: vuot chi so index
    zerodivisionerror: chia cho 0
    typeerror: sai kieu dl
    findnotfounderror: k ton tai file
    attributeerror: goi pthuc k ton tai
    
"""

logging.basicConfig(
    filename="arena_tickets.log",   #Ghi log vào file:
    level=logging.INFO,             # Chỉ ghi từ mức INFO trở lên.
    format="%(asctime)s - %(levelname)s - %(message)s"
)
ticket_db = [
    {"ticket_id": "T01", "buyer_name": "Nguyen Van A", "price": 500.0, "status": "Booked", "seat": ("A", 1)},
    {"ticket_id": "T02", "buyer_name": "Tran Thi B", "price": 300.0, "status": "Cancelled", "seat": ("B", 5)},
    {"ticket_id": "T03", "buyer_name": "Le Van C", "price": 500.0, "status": "Booked", "seat": ("A", 2)}
]

def display_tickets(tickets):
    if len(tickets)==0:
        print("k co ve nao trong danh sach")
        return
    print('DANH SACH VE:')
    print("MA VE | TEN KHACH HANG | GIA VE | CHO NGOI | TRANG THAI: ")
    for ticket in tickets:
        try:
            seat_0=f"{ticket["seat"][0]}-{ticket["seat"][1]}"
            status=ticket["status"]
            if status=="Cancelled":
                status+=" [DA HUY] "
            print(f"MA VE: {ticket["ticket_id"]}"
                  f"TEN KHACH HANG: {ticket["buyer_name"]} "
                  f"GIA VE: {ticket["price"]}"
                  f"CHO NGOI: {seat_0}"
                  f"TRANG THAI: {status}")
        except KeyError as e:
            print("LỖI VÉ ĐANG BỊ THIẾU DU LIEU, VUI LONG KTRA LAI.")
            logging.error(e)
    logging.info("User viewed ticket list")


def book_ticket(tickets):

    ma_new=input("yeu cau nhap ma moi can them")

    for i in tickets:
        if ma_new==i["ticket_id"]:
            print(f"LOI MA VE {ma_new} DA TON TAI")
            logging.warning(f"Duplicate ticket ID entered {ma_new}")
            return

    new_name=input("MOI BAN NHAP TEN VE: ")
    while True:
        try:
            price_ticket_new=input("YEU CAU NHAP GIA VE MOI")
            if float(price_ticket_new)>0:
                break
            print("Giá vé phải lớn hơn 0. Vui lòng nhập lại.")
        except ValueError :
            print("Giá vé phải là số. Vui lòng nhập lại.")
            logging.warning("Invalid price input while booking ticket")

    area=input("NHAP KHU VUC MOI ").upper()

    while True:
        try:
            seat_number=int(input("YEU CAU NHAP  Số ghế MOI: "))
            break

        except ValueError :
            print(" Số ghế.phải là số. Vui lòng nhập lại.")
    tickets.append({
        "ticket_id": ma_new,
        "buyer_name": new_name,
        "price": float(price_ticket_new),
        "status": "Booked",
        "seat": (area, seat_number)
    })

    logging.info(f"Booked new ticket {ma_new} for {new_name}")

def change_seat(tickets):
    ma_change=input("YEU CAU NHAP MA CAN THAY DOI: ")
    flag=0
    for i in tickets:
        if ma_change == i["ticket_id"]:
            flag=1
            new_seat=input("Nhập khu vực ghế mới: ").upper()
            while True:
                try:
                    number_new=int(input("Nhập số ghế mới:"))
                    break
                except ValueError:
                    print("Số ghế phải là số nguyên. Vui lòng nhập lại.")
            i["seat"]=(new_seat,number_new)
            print(f"Thành công: Đã đổi chỗ vé {ma_change} sang {new_seat}-{number_new}")
            logging.info(f"Seat changed for ticket {ma_change} to {new_seat}-{number_new}")
    if flag==0:
        print(f"Không tìm thấy vé mang mã {ma_change}")
        logging.warning(f" Change seat failed - Ticket {ma_change} not found")

def cancel_ticket(tickets):
    cancel_ticket=input("YEU CAU NHAP MA VE CAN HUY: ")
    flag=0
    for i in tickets:
        if cancel_ticket==i["ticket_id"]:
            flag=1
            if i["status"] =="Cancelled":
                print(f" Vé {cancel_ticket} đã ở trạng thái Cancelled trước đó.")
            else:
                i["status"] = "Cancelled"
                print(f"Thành công: Vé {cancel_ticket}đã được hủy.")
                logging.warning(f"Ticket {cancel_ticket} has been cancelled.")
    if flag==0:
        print(f"Không tìm thấy vé mang mã {cancel_ticket}")
        logging.warning(f"Cancel ticket failed - Ticket {cancel_ticket}not found")

def calculate_total_revenue(ticket_list) -> float :
    total=0.00
    for ticket in ticket_list:
        if ticket["status"] =="Booked":
            total+= ticket["price"]
            # o day neu dung get thi se loi vi get  tra ra None co the dung get("price",0) de gan gia tri mac dinh la 0
    return total


def calculate_revenue(tickets):
    print("--- BÁO CÁO DOANH THU ---")
    cancel=0
    book=0
    try:
        for i in tickets:
            if i["status"] == "Booked":
                book+=1
            elif i["status"] == "Cancelled":
                cancel+=1
        total=calculate_total_revenue(tickets)
        print(f"Tổng số vé đã đặt: {book}")
        print(f"Tổng số vé đã hủy: {cancel}")
        print(f"Tổng doanh thu hợp lệ:{total}")
        logging.info(f"Revenue report generated. Total: {total}")

    except KeyError as e :
        print("Lỗi: Một vé đang bị thiếu dữ liệu doanh thu.")
        print(f"Tổng doanh thu hợp lệ: 0.00")
        logging.error(f"- ERROR - Missing key while calculating revenue: {e}")








if __name__== "__main__":
    while True:
        choose=input("""
        === HỆ THỐNG QUẢN LÝ VÉ RIKKEI ESPORTS ===
        1. Xem danh sách vé đã bán
        2. Đặt vé mới
        3. Đổi chỗ ngồi (Cập nhật vé)
        4. Hủy vé
        5. Báo cáo doanh thu
        6. Thoát chương trình
        NHAP LUA CHON TU 1->6
        """)
        match choose:
            case "1":
                display_tickets(ticket_db)
            case "2":
                book_ticket(ticket_db)
            case "3":
                change_seat(ticket_db)
            case "4":
                cancel_ticket(ticket_db)
            case "5":
                calculate_revenue(ticket_db)
            case "6":
                break