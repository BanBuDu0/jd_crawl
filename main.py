import generate_comments
import spir
import db_control


def show_hotcomments(item: {}):
    ci = spir.hotcomments(item)
    generate_comments.generateByfrequent(ci)


def show_pcomments(item: {}):
    ci = spir.pcomments(item)
    generate_comments.generateByText(ci)


if __name__ == '__main__':
    item = db_control.best()
    # item = db_control.minPrice()
    show_hotcomments(item)
    show_pcomments(item)

