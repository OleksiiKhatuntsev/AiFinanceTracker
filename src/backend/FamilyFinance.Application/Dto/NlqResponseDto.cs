namespace FamilyFinance.Application.Dto;

public record NlqResponseDto(string Answer, IReadOnlyList<TransactionDto>? Data);
