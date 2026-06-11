import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

ERR_E01 = "[Lỗi] (ERR-E01): Mã thiết bị này không tồn tại trong danh sách hệ thống!"
ERR_E02 = "[Lỗi] (ERR-E02): Số liệu lỗi! Chỉ số mới không được nhỏ hơn chỉ số cũ!"
ERR_E03 = "[Lỗi] (ERR-E03): Định dạng không hợp lệ! Chỉ số điện phải là số lớn hơn hoặc bằng 0!"
ERR_E04 = "[Lỗi] (ERR-E04): Thao tác bị hủy! Thiết bị này đã được kích hoạt trạng thái OVERLOAD từ trước!"
ERR_E05 = "[Lỗi] (ERR-E05): Lựa chọn sai! Vui lòng nhập đúng số thứ tự chức năng từ 1 đến 5!"

SAMPLE_DEVICES = [
    {
        "id": "M01",
        "location": "Mechanical Shop A",
        "old_index": 1000,
        "new_index": 7000,
        "status": "Normal"
    },
    {
        "id": "M02",
        "location": "Assembly Line B",
        "old_index": 2500,
        "new_index": 5500,
        "status": "Normal"
    },
    {
        "id": "M03",
        "location": "Packaging Area",
        "old_index": 1200,
        "new_index": 8200,
        "status": "Normal"
    }
]


def find_device_by_id(devices_list, device_id):
    for device in devices_list:
        if device["id"] == device_id:
            return device
    return None


def input_non_negative_number(message):
    while True:
        try:
            value = float(input(message).strip())

            if value < 0:
                print(ERR_E03)
                logger.error(ERR_E03)
                continue

            return value

        except ValueError:
            print(ERR_E03)
            logger.error(ERR_E03)


def show_menu():
    print("""
========================================
SMART ENERGY MONITOR - PHÒNG CƠ ĐIỆN
========================================
1. Xem danh sách thiết bị giám sát
2. Cập nhật chỉ số điện tiêu thụ
3. Kích hoạt trạng thái cảnh báo quá tải
4. Tính tổng lượng điện & Chi phí năng lượng
5. Thoát chương trình
""")


def show_devices(devices_list):
    logger.debug(f"Đang hiển thị danh sách {len(devices_list)} thiết bị")

    if not devices_list:
        print("Hệ thống hiện chưa có thiết bị giám sát nào!")
        return

    print(f'{"MÃ THIẾT BỊ":<15}{"VỊ TRÍ PHÂN XƯỞNG":<30}{"CHỈ SỐ CŨ":>15}{"CHỈ SỐ MỚI":>15}{"TRẠNG THÁI":>15}')
    print("-" * 90)

    for device in devices_list:
        print(f'{device["id"]:<15}{device["location"]:<30}{device["old_index"]:>15.2f}{device["new_index"]:>15.2f}{device["status"]:>15}')


def update_indices(devices_list):
    logger.debug("Đang thực hiện cập nhật chỉ số điện")

    if not devices_list:
        print("Hệ thống hiện chưa có thiết bị giám sát nào!")
        return

    device_id = input("Nhập mã thiết bị cần cập nhật chỉ số: ").strip().upper()
    device = find_device_by_id(devices_list, device_id)

    if not device:
        print(ERR_E01)
        logger.error(ERR_E01)
        return

    old_index = input_non_negative_number("Nhập chỉ số cũ: ")

    while True:
        new_index = input_non_negative_number("Nhập chỉ số mới: ")

        if new_index < old_index:
            print(ERR_E02)
            logger.error(ERR_E02)
            continue

        break

    device["old_index"] = old_index
    device["new_index"] = new_index

    logger.info(f"[Thành công]: Đã check-in số liệu cho thiết bị {device_id}")
    print(f"[Thành công]: Đã cập nhật chỉ số điện cho thiết bị {device_id}")


def trigger_overload_alert(devices_list):
    logger.debug("Đang kích hoạt trạng thái cảnh báo quá tải")

    if not devices_list:
        print("Hệ thống hiện chưa có thiết bị giám sát nào!")
        return

    device_id = input("Nhập mã thiết bị cần cập nhật trạng thái: ").strip().upper()
    device = find_device_by_id(devices_list, device_id)

    if not device:
        print(ERR_E01)
        logger.error(ERR_E01)
        return

    if device["status"] == "Overload":
        print(ERR_E04)
        logger.error(ERR_E04)
        return

    consumption = device["new_index"] - device["old_index"]

    if consumption > 5000:
        device["status"] = "Overload"

        logger.warning(
            f"[Cảnh báo]: Thiết bị {device_id} đã vượt ngưỡng tiêu thụ an toàn, chuyển sang OVERLOAD!"
        )

        print(f"[Thành công]: Thiết bị {device_id} đã được chuyển sang trạng thái OVERLOAD")
    else:
        print(f"Thiết bị {device_id} chưa vượt ngưỡng tiêu thụ an toàn.")


def calculate_energy_financials(devices_list):
    logger.debug(f"Đang tính toán chi phí năng lượng cho {len(devices_list)} thiết bị")

    if not devices_list:
        return 0.0, 0.0, 0.0

    total_kwh = 0

    for device in devices_list:
        total_kwh += device["new_index"] - device["old_index"]

    discount_percent = 3.0 if total_kwh >= 50000 else 0.0
    total_cost = total_kwh * 3000
    final_cost = total_cost * (100 - discount_percent) / 100

    return total_kwh, discount_percent, final_cost


def show_energy_financials(devices_list):
    total_kwh, discount_percent, final_cost = calculate_energy_financials(devices_list)

    print(f"""
----- BÁO CÁO NĂNG LƯỢNG -----
Tổng điện tiêu thụ: {total_kwh:,.2f} kWh
Tỷ lệ chiết khấu: {discount_percent}%
Tổng tiền sau chiết khấu: {final_cost:,.0f} VND
""")


def main():
    devices_list = [device.copy() for device in SAMPLE_DEVICES]

    while True:
        show_menu()

        try:
            choice = int(input("Mời chọn chức năng (1-5): "))

            match choice:
                case 1:
                    show_devices(devices_list)

                case 2:
                    update_indices(devices_list)

                case 3:
                    trigger_overload_alert(devices_list)

                case 4:
                    show_energy_financials(devices_list)

                case 5:
                    print("Thoát chương trình thành công!")
                    break

                case _:
                    print(ERR_E05)
                    logger.error(ERR_E05)

        except ValueError:
            print(ERR_E05)
            logger.error(ERR_E05)


if __name__ == "__main__":
    main()
