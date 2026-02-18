using FamilyFinance.Domain.Exceptions;

namespace FamilyFinance.Domain.Entities;

public class Transaction
{
    public Guid Id { get; private set; }
    public decimal Amount { get; private set; }
    public string Currency { get; private set; }
    public string Merchant { get; private set; }
    public DateTime Date { get; private set; }
    public string Category { get; private set; } = null!;

    public Transaction(decimal amount, string currency, string merchant, DateTime date, string category)
    {
        if (amount < 0)
        {
            throw new InvalidAmountException(amount);
        }

        if (string.IsNullOrWhiteSpace(currency))
        {
            throw new EmptyCurrencyException();
        }

        if (string.IsNullOrWhiteSpace(merchant))
        {
            throw new EmptyMerchantException();
        }

        if (string.IsNullOrWhiteSpace(category))
        {
            throw new EmptyCategoryException();
        }

        Id = Guid.NewGuid();
        Amount = amount;
        Currency = currency.ToUpper();
        Merchant = merchant;
        Date = date;
        Category = category;
    }
}