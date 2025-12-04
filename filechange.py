import os


def rename_skill1_files():
    iori_folder = r'C:\Users\Admin\Desktop\2DGP\2dgp_project\iori'

    # iori 폴더의 모든 파일 가져오기
    files = os.listdir(iori_folder)

    # b35로 시작하는 파일만 필터링
    b35_files = [f for f in files if f.startswith('9464f67f67d0418e9dca853463ff6e49i8l7VTG2uSqOBhbV-')]

    for old_name in b35_files:
        # 숫자 부분 추출 (파일명에서 마지막 '-' 이후부터 '.png' 이전까지)
        number = old_name.split('-')[-1].replace('.png', '')

        # 새 파일명 생성
        new_name = f'iori_dead_{number}.png'

        # 전체 경로 생성
        old_path = os.path.join(iori_folder, old_name)
        new_path = os.path.join(iori_folder, new_name)

        # 파일명 변경
        os.rename(old_path, new_path)
        print(f'{old_name} -> {new_name}')

    print(f'\n총 {len(b35_files)}개 파일 변경 완료')


if __name__ == '__main__':
    rename_skill1_files()
