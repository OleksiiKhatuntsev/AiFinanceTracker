using FamilyFinance.Application.Dto;
using FamilyFinance.Application.Exceptions;
using FamilyFinance.Application.Interfaces;

using Microsoft.AspNetCore.Mvc;

namespace FamilyFinance.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class NlqController(IAiService aiService) : ControllerBase
{
    [HttpPost("ask")]
    public async Task<IActionResult> Ask(NlqRequestDto request, CancellationToken cancellationToken = default)
    {
        try
        {
            var response = await aiService.AskAsync(request, cancellationToken);
            return Ok(response);
        }
        catch (AiServiceUnavailableException)
        {
            return StatusCode(503, new { error = "The AI service is currently unavailable. Please try again later." });
        }
    }
}
