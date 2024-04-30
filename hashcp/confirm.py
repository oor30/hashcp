def confirm(message: str) -> bool:
    '''メッセージを出力し、yesまたはnoの入力を受け取り、bool値で返す。
    '''
    while True:
        choice = input(message).lower()
        if choice in ['y', 'ye', 'yes']:
            return True
        elif choice in ['n', 'no']:
            print('canceled')
            return False
        else:
            print('invalid input detected')
            continue