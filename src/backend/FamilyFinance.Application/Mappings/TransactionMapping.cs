using FamilyFinance.Application.Dto;
using FamilyFinance.Domain.Entities;

namespace FamilyFinance.Application.Mappings;

public static class TransactionMapping
{
    public static TransactionDto ToDto(this Transaction entity)
    {
        return new TransactionDto(
            entity.Id,
            entity.Amount,
            entity.Currency,
            entity.Merchant,
            entity.Date,
            "Uncategorized",
            $"{entity.Amount:F2} {entity.Currency}"
        );
    }

    public static Transaction ToEntity(this TransactionDto dto)
    {
        return new Transaction(
            dto.Amount,
            dto.Currency,
            dto.Merchant,
            dto.Date
        );
    }
}