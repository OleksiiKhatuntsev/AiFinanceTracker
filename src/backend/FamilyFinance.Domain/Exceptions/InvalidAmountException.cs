namespace FamilyFinance.Domain.Exceptions;

public class InvalidAmountException(decimal amount)
    : DomainException($"Amount cannot be negative. Value provided: {amount}")
{
}