namespace FamilyFinance.Application.Dto;

public record TransactionDto(
    Guid Id,
    decimal Amount,
    string Currency,
    string Merchant,
    DateTime Date,
    string Category,
    string FormattedAmount
);
