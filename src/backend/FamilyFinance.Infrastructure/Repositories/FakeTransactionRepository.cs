using FamilyFinance.Domain.Entities;
using FamilyFinance.Domain.Repositories;

namespace FamilyFinance.Infrastructure.Repositories;

public class FakeTransactionRepository : ITransactionRepository
{
    private readonly List<Transaction> _transactions =
    [
        new(150.00m, "USD", "Amazon", new DateTime(2026, 1, 5, 10, 30, 0, DateTimeKind.Utc)),
        new(12.99m, "USD", "Netflix", new DateTime(2026, 1, 10, 8, 0, 0, DateTimeKind.Utc)),
        new(5.75m, "EUR", "Starbucks", new DateTime(2026, 1, 12, 14, 15, 0, DateTimeKind.Utc)),
        new(89.50m, "PLN", "Walmart", new DateTime(2026, 1, 18, 16, 45, 0, DateTimeKind.Utc)),
        new(1.99m, "USD", "Apple", new DateTime(2026, 1, 20, 9, 0, 0, DateTimeKind.Utc)),
        new(59.99m, "EUR", "Steam", new DateTime(2026, 1, 22, 20, 30, 0, DateTimeKind.Utc)),
        new(23.40m, "GBP", "Uber", new DateTime(2026, 1, 25, 7, 10, 0, DateTimeKind.Utc)),
        new(320.00m, "USD", "Airbnb", new DateTime(2026, 1, 28, 12, 0, 0, DateTimeKind.Utc)),
        new(8.49m, "EUR", "McDonald's", new DateTime(2026, 2, 1, 13, 30, 0, DateTimeKind.Utc)),
        new(9.99m, "USD", "Spotify", new DateTime(2026, 2, 5, 6, 0, 0, DateTimeKind.Utc)),
    ];

    public IReadOnlyList<Transaction> GetAll() => _transactions.AsReadOnly();
}
