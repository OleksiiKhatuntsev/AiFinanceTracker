namespace FamilyFinance.Domain.Entities;

using FamilyFinance.Domain.Exceptions;

public class Transaction
{
    public Guid Id { get; private set; }
    public decimal Amount { get; private set; }
    public string Currency { get; private set; }

    private Transaction() { }

    public Transaction(decimal amount, string currency)
    {
        if (amount < 0)
        {
            throw new DomainException("Amount cannot be negative");
        }
        if (string.IsNullOrEmpty(currency))
        {
            throw new DomainException("Where money, Lebovski?");
        }

        Id = Guid.NewGuid();
        Amount = amount;
        Currency = currency;
    }
}