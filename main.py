import logging

logging.basicConfig(
    filename='tournament_app.log',
    level=logging.INFO,
    format='[%(asctime)s] - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

matches = [
    {
        "match_id": "M01",
        "team_a": "T1",
        "team_b": "GenG",
        "score_a": 2,
        "score_b": 1,
        "status": "Completed"
    },
    {
        "match_id": "M02",
        "team_a": "JDG",
        "team_b": "BLG",
        "score_a": 0,
        "score_b": 0,
        "status": "Pending"
    }
]

def display_matches(match_list):
    if not match_list:
        print("Hiện chưa có trận đấu nào trong hệ thống.")
        logging.info("User viewed the match list (empty).")
        return

    print("\n--- LỊCH THI ĐẤU & KẾT QUẢ ---")
    print(f"{'Mã trận':<10} | {'Đội A':<15} | {'Đội B':<15} | {'Tỷ số':<7} | {'Trạng thái'}")
    print("-" * 70)
    for match in match_list:
        try:
            score_str = f"{match['score_a']}-{match['score_b']}"
            print(f"{match['match_id']:<10} | {match['team_a']:<15} | {match['team_b']:<15} | {score_str:<7} | {match['status']}")
        except KeyError as e:
            logging.error(f"Missing data key when displaying match: {e}")
            
    logging.info("User viewed the match list.")

def add_match(match_list):
    print("\n--- THÊM TRẬN ĐẤU MỚI ---")
    match_id = input("Nhập mã trận đấu: ").strip()
    
    if not match_id:
        print("\nMã trận đấu không được để trống.")
        logging.warning("User tried to add a match with empty match ID.")
        return

    # Kiểm tra trùng lặp
    for match in match_list:
        if match["match_id"] == match_id:
            print(f"\nLỗi: Mã trận đấu {match_id} đã tồn tại.")
            logging.warning(f"Match ID {match_id} already exists.")
            return

    team_a = input("Nhập tên Đội A: ").strip()
    team_b = input("Nhập tên Đội B: ").strip()

    if not team_a or not team_b:
        print("\nTên đội không được để trống.")
        logging.warning("User tried to add a match with empty team name.")
        return

    new_match = {
        "match_id": match_id,
        "team_a": team_a,
        "team_b": team_b,
        "score_a": 0,
        "score_b": 0,
        "status": "Pending"
    }
    match_list.append(new_match)
    print(f"\nThành công: Đã thêm trận đấu {match_id}.")
    logging.info(f"Match {match_id} added successfully")

def get_valid_score(team_name):
    while True:
        score_input = input(f"Nhập điểm {team_name}: ")
        try:
            score = int(score_input)
            if score < 0:
                print("\nĐiểm số phải lớn hơn hoặc bằng 0.")
                logging.error(f"Negative score input detected: {score}")
                continue
            return score
        except ValueError as e:
            print("\nĐiểm số phải là số nguyên. Vui lòng nhập lại.")
            logging.error(f"Invalid score input. Error: invalid literal for int() with base 10: '{score_input}'")

def update_score(match_list):
    print("\n--- CẬP NHẬT TỶ SỐ TRẬN ĐẤU ---")
    match_id = input("Nhập mã trận đấu cần cập nhật: ").strip()

    target_match = None
    for match in match_list:
        if match["match_id"] == match_id:
            target_match = match
            break

    if not target_match:
        print(f"\nKhông tìm thấy trận đấu mang mã {match_id}.")
        logging.warning(f"User tried to update non-existing match {match_id}")
        return

    print(f"\nTrận đấu: {target_match['team_a']} vs {target_match['team_b']} ({target_match['status']})")
    
    score_a = get_valid_score("Đội A")
    score_b = get_valid_score("Đội B")

    if score_a == 0 and score_b == 0:
        confirm = input("\nTỷ số đang là 0-0. Trọng tài có xác nhận trận đã hoàn thành không? (y/n): ").strip().lower()
        if confirm == 'y':
            target_match['status'] = "Completed"
        else:
            target_match['status'] = "Pending"
    else:
        target_match['status'] = "Completed"

    target_match['score_a'] = score_a
    target_match['score_b'] = score_b

    print(f"\nThành công: Đã cập nhật tỷ số trận đấu {match_id}.")
    logging.info(f"Match {match_id} score updated successfully")

def determine_winner(match):
    try:
        if match["status"] == "Pending":
            return "Not Started"
        
        score_a = match["score_a"]
        score_b = match["score_b"]
        
        if score_a > score_b:
            return match["team_a"]
        elif score_b > score_a:
            return match["team_b"]
        else:
            return "Draw"
    except KeyError as e:
        logging.error(f"KeyError in determine_winner: Missing {e}")
        return "Data Error"

def generate_report(match_list):
    print("\n--- BÁO CÁO THỐNG KÊ GIẢI ĐẤU ---")
    completed_count = 0
    
    for match in match_list:
        if match.get("status") == "Completed":
            winner = determine_winner(match)
            print(f"{match['match_id']}: {match['team_a']} {match['score_a']}-{match['score_b']} {match['team_b']} | Kết quả: {winner}")
            completed_count += 1

    if completed_count == 0:
        print("Chưa có trận đấu nào hoàn thành.")
        
    print(f"\nTổng số trận đã hoàn thành: {completed_count}")
    logging.info("User generated tournament report.")

def main():
    while True:
        print("\n===== HỆ THỐNG QUẢN LÝ GIẢI ĐẤU RIKKEI ESPORTS =====")
        print("1. Hiển thị lịch thi đấu & Kết quả")
        print("2. Thêm trận đấu mới")
        print("3. Cập nhật tỷ số trận đấu")
        print("4. Báo cáo thống kê")
        print("5. Thoát chương trình")
        print("==================================================")
        
        choice = input("Chọn chức năng (1-5): ")
        match choice:
            case "1":
                display_matches(matches)
            case "2":
                add_match(matches)
            case "3":
                update_score(matches)
            case "4":
                generate_report(matches)
            case  "5":
                logging.info("System closed. Exiting program.")
                print("Đã thoát chương trình.")
                break
            case _:
                print("Lựa chọn không hợp lệ. Vui lòng chọn từ 1 đến 5.")
                logging.warning("Invalid menu choice selected (out of range).")

if __name__ == "__main__":
    main()
