def cyberloop(game='Cyberpunk', iterations=2077):
    cyberlist = [(f'{str(game)} {i}, ') for i in range(1, iterations - 1)]
    print('Guys, do I have to play', ''.join(cyberlist), f'and {str(game)} {iterations - 1} before playing {str(game)} {iterations}?')


if __name__ == '__main__':
    cyberloop('Metro', 2033)
