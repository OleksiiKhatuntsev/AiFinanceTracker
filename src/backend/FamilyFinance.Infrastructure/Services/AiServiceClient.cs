using System.Net.Http.Json;
using System.Text.Json;

using FamilyFinance.Application.Dto;
using FamilyFinance.Application.Exceptions;
using FamilyFinance.Application.Interfaces;

namespace FamilyFinance.Infrastructure.Services;

public class AiServiceClient(HttpClient httpClient) : IAiService
{
    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNameCaseInsensitive = true,
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
    };

    public async Task<NlqResponseDto> AskAsync(NlqRequestDto request, CancellationToken cancellationToken = default)
    {
        try
        {
            HttpResponseMessage response = await httpClient.PostAsJsonAsync("/nlq/ask", request, JsonOptions, cancellationToken);
            _ = response.EnsureSuccessStatusCode();

            NlqResponseDto? result = await response.Content.ReadFromJsonAsync<NlqResponseDto>(JsonOptions, cancellationToken);
            return result!;
        }
        catch (HttpRequestException ex)
        {
            throw new AiServiceUnavailableException(ex);
        }
    }
}
