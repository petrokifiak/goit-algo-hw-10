import timeit


COINS = [50, 25, 10, 5, 2, 1]


def find_coins_greedy(amount: int) -> dict[int, int]:
    """
    Жадібний алгоритм видачі решти.
    Спочатку вибирає найбільші доступні номінали монет.
    """
    result = {}
    for coin in COINS:
        if amount >= coin:
            coin_count = amount // coin
            result[coin] = coin_count
            amount %= coin
        if amount == 0:
            break
    return result


def find_min_coins(amount: int) -> dict[int, int]:
    """
    Алгоритм динамічного програмування для пошуку мінімальної кількості монет.
    Побудова таблиці знизу вгору (bottom-up).
    """
    # min_coins[i] зберігає мінімальну кількість монет для суми i
    min_coins = [0] + [float("inf")] * amount
    # last_coin[i] зберігає останню додану монету для відновлення шляху
    last_coin = [0] * (amount + 1)

    for current_sum in range(1, amount + 1):
        for coin in COINS:
            if current_sum >= coin and min_coins[current_sum - coin] + 1 < min_coins[current_sum]:
                min_coins[current_sum] = min_coins[current_sum - coin] + 1
                last_coin[current_sum] = coin

    # Відновлення словника з номіналами та їх кількістю
    result = {}
    remaining_sum = amount
    while remaining_sum > 0:
        coin = last_coin[remaining_sum]
        result[coin] = result.get(coin, 0) + 1
        remaining_sum -= coin

    return result


if __name__ == "__main__":
    # 1. Перевірка на прикладі з умови (сума 113)
    test_amount = 113
    print(f"Сума: {test_amount}")
    print(f"Жадібний алгоритм:       {find_coins_greedy(test_amount)}")
    print(f"Динамічне програмування: {find_min_coins(test_amount)}\n")

    # 2. Порівняння часу виконання на різних сумах
    test_sums = [113, 1_000, 10_000, 50_000]
    print(f"{'Сума':<10} | {'Greedy (сек)':<15} | {'Dynamic programming (сек)':<27}")
    print("-" * 58)

    for target_sum in test_sums:
        greedy_total_time = timeit.timeit(lambda: find_coins_greedy(target_sum), number=100)
        dynamic_programming_total_time = timeit.timeit(lambda: find_min_coins(target_sum), number=10)
        # Нормалізуємо час до одного запуску
        print(
            f"{target_sum:<10} | {greedy_total_time / 100:<15.8f} "
            f"| {dynamic_programming_total_time / 10:<27.8f}"
        )
