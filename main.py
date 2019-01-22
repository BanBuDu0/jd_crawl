import generate_comments
import spir
import db_control


def show_hotcomments(item: {}):
    ci = spir.hotcomments(item)
    path = generate_comments.generateByfrequent(ci)
    return path


def show_pcomments(item: {}):
    ci = ""
    for i in spir.pcomments(item):
        ci += i + " " 
    path = generate_comments.generateByText(ci)
    return path


if __name__ == '__main__':
    item = db_control.minPrice()
    # item = db_control.minPrice()
    print(show_hotcomments(item))
    print(show_pcomments(item))
