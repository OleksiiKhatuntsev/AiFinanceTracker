using FamilyFinance.Application.Dto;

namespace FamilyFinance.Application.Interfaces;

public interface IAiService
{
    Task<NlqResponseDto> AskAsync(NlqRequestDto request, CancellationToken cancellationToken = default);
}
