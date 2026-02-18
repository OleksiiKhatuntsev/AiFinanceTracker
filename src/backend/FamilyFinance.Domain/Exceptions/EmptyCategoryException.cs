namespace FamilyFinance.Domain.Exceptions;

public class EmptyCategoryException()
    : DomainException("Category is required and cannot be empty.")
{ }
