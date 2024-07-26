from copy import deepcopy


def generate_unique_slugify(obj, value):
    """
    유니크한 슬러그 필드 생성
    -> e.g) "테스트-아티클" -> "테스트-아티클2"
    """
    num = 1
    slug = deepcopy(value)

    while obj.objects.filter(slug=slug).exists():
        num += 1
        slug = f"{value}{num}"

        if num == 10:
            break
    return slug
