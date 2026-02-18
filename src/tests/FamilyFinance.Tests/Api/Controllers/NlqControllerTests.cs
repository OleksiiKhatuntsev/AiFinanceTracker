using FamilyFinance.Api.Controllers;
using FamilyFinance.Application.Dto;
using FamilyFinance.Application.Exceptions;
using FamilyFinance.Application.Interfaces;

using Microsoft.AspNetCore.Mvc;

using Moq;

namespace FamilyFinance.Tests.Api.Controllers;

public class NlqControllerTests
{
    private readonly Mock<IAiService> _aiServiceMock = new();
    private readonly NlqController _controller;

    public NlqControllerTests()
    {
        _controller = new NlqController(_aiServiceMock.Object);
    }

    [Fact]
    public async Task Ask_ReturnsOk_WithResponse_WhenAiServiceResponds()
    {
        // Arrange
        var request = new NlqRequestDto("How much did we spend on shopping in January?");
        var expectedResponse = new NlqResponseDto("You spent $89.50 on shopping in January.", []);

        _aiServiceMock
            .Setup(s => s.AskAsync(request, It.IsAny<CancellationToken>()))
            .ReturnsAsync(expectedResponse);

        // Act
        var result = await _controller.Ask(request);

        // Assert
        var okResult = Assert.IsType<OkObjectResult>(result);
        Assert.Equal(expectedResponse, okResult.Value);
    }

    [Fact]
    public async Task Ask_Returns503_WhenAiServiceIsUnavailable()
    {
        // Arrange
        var request = new NlqRequestDto("How much did we spend?");

        _aiServiceMock
            .Setup(s => s.AskAsync(It.IsAny<NlqRequestDto>(), It.IsAny<CancellationToken>()))
            .ThrowsAsync(new AiServiceUnavailableException());

        // Act
        var result = await _controller.Ask(request);

        // Assert
        var statusResult = Assert.IsType<ObjectResult>(result);
        Assert.Equal(503, statusResult.StatusCode);
    }

    [Fact]
    public async Task Ask_CallsAiService_ExactlyOnce_WithCorrectRequest()
    {
        // Arrange
        var request = new NlqRequestDto("What are my recent transactions?");

        _aiServiceMock
            .Setup(s => s.AskAsync(request, It.IsAny<CancellationToken>()))
            .ReturnsAsync(new NlqResponseDto("Here are your recent transactions.", []));

        // Act
        await _controller.Ask(request);

        // Assert
        _aiServiceMock.Verify(s => s.AskAsync(request, It.IsAny<CancellationToken>()), Times.Once);
    }
}
