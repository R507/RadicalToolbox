import traceback


def main():
    try:
        raise ValueError("watafuck")
    except Exception as exc:
        traceback.print_tb(exc)


if __name__ == '__main__':
    main()
