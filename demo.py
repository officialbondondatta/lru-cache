from lru_cache import Cache


def main():
    cache = Cache(2)
    print('LRU CACHE | capacity = 2')
    print('Order shown below: least recently used -> most recently used\n')

    def put(key, value):
        before = dict(cache.items_lru_to_mru())
        result = cache.put(key, value)
        after = cache.items_lru_to_mru()
        evicted = [k for k in before if k not in dict(after)]
        print(f'put({key!r}, {value}) -> {result}')
        if evicted:
            print(f'  LRU eviction: {evicted[0]!r} (value={before[evicted[0]]})')
        print(f'  State: {after}')

    def get(key, expected):
        result = cache.get(key)
        print(f'get({key!r}) -> {result}')
        print(f'  State: {cache.items_lru_to_mru()}')
        assert result == expected, (key, result, expected)

    put('A', 10)
    put('B', 20)
    get('A', 10)
    put('C', 30)
    get('B', -1)
    get('C', 30)
    get('A', 10)
    print('\nUpdate existing key:')
    put('C', 300)
    get('C', 300)
    print('\nPASS: all example return values match expectations.')


if __name__ == '__main__':
    main()
