namespace FamilyFinance.Domain.Exceptions;

public class EmptyCurrencyException()
    : DomainException("Currency code is required and cannot be empty.")
{ }