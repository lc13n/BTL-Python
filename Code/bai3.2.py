import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse

def radar_chart(player1_stats, player2_stats, attributes):
    num_vars = len(attributes)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    player1_stats = np.concatenate((player1_stats, [player1_stats[0]]))
    player2_stats = np.concatenate((player2_stats, [player2_stats[0]]))
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, player1_stats, color='blue', alpha=0.25, label='Player 1')
    ax.fill(angles, player2_stats, color='red', alpha=0.25, label='Player 2')
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(attributes)
    plt.legend(loc='upper right')
    plt.title('So sánh cầu thủ')
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Vẽ biểu đồ radar so sánh cầu thủ.')
    parser.add_argument('--p1', required=True, help='Tên cầu thủ thứ nhất')
    parser.add_argument('--p2', required=True, help='Tên cầu thủ thứ hai')
    parser.add_argument('--Attribute', required=True, help='Danh sách các chỉ số cần so sánh, cách nhau bởi dấu phẩy (att1,att2,...,att_n)')
    
    args = parser.parse_args()

    # Đọc dữ liệu từ file CSV với dấu phân cách là dấu chấm phẩy
    data = pd.read_csv('results.csv', sep=';')

    player1 = args.p1
    player2 = args.p2
    attributes = args.Attribute.split(',')

    # Kiểm tra xem cầu thủ có tồn tại trong dữ liệu không
    if player1 not in data['Player'].values or player2 not in data['Player'].values:
        print(f"Một hoặc cả hai cầu thủ '{player1}' và '{player2}' không tồn tại trong dữ liệu.")
        return

    # Lấy thông tin chỉ số của cầu thủ
    player1_stats = data.loc[data['Player'] == player1, attributes].values.flatten()
    player2_stats = data.loc[data['Player'] == player2, attributes].values.flatten()

    # Vẽ biểu đồ radar
    radar_chart(player1_stats, player2_stats, attributes)

if __name__ == '__main__':
    main()
