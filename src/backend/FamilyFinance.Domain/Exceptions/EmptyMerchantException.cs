namespace FamilyFinance.Domain.Exceptions;

public class EmptyMerchantException()
    : DomainException("Merchant name is required and cannot be empty.")
{ }
