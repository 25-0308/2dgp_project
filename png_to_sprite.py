from PIL import Image
import os


def create_sprite_sheet(folder_path, prefix, output_name, frame_count):
    """
    여러 PNG 파일을 하나의 스프라이트 시트로 합치는 함수

    Args:
        folder_path: 이미지가 있는 폴더 경로
        prefix: 파일명 접두사 (예: 'iori_skill1_')
        output_name: 출력 파일명 (예: 'iori_skill1_sprite.png')
        frame_count: 프레임 개수 (예: 44)
    """
    # 첫 번째 이미지로 크기 확인
    first_image_path = os.path.join(folder_path, f'{prefix}0.png')
    first_img = Image.open(first_image_path)
    frame_width, frame_height = first_img.size

    # 스프라이트 시트 생성 (가로로 배열)
    sprite_sheet = Image.new('RGBA', (frame_width * frame_count, frame_height))

    # 각 프레임을 스프라이트 시트에 붙이기
    for i in range(frame_count):
        img_path = os.path.join(folder_path, f'{prefix}{i}.png')
        if os.path.exists(img_path):
            img = Image.open(img_path)
            sprite_sheet.paste(img, (frame_width * i, 0))
            print(f'프레임 {i} 추가 완료')
        else:
            print(f'경고: {img_path} 파일을 찾을 수 없습니다.')

    # 스프라이트 시트 저장
    output_path = os.path.join(folder_path, output_name)
    sprite_sheet.save(output_path)
    print(f'\n스프라이트 시트 생성 완료: {output_path}')
    print(f'크기: {sprite_sheet.size[0]} x {sprite_sheet.size[1]} 픽셀')


# 사용 예시
if __name__ == '__main__':
    iori_folder = r'C:\Users\00rhk\Desktop\2DGP\2dgp_project\kyo'

    # iori_skill1 스프라이트 시트 생성
    create_sprite_sheet(
        folder_path=iori_folder,
        prefix='kyo_skill2_',
        output_name='kyo_skill2_sprite.png',
        frame_count=19
    )
