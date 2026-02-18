using System.Net;
using System.Net.Http.Json;

using FamilyFinance.Application.Dto;
using FamilyFinance.Application.Exceptions;
using FamilyFinance.Infrastructure.Services;

using Moq;
using Moq.Protected;

namespace FamilyFinance.Tests.Infrastructure.Services;

public class AiServiceClientTests
{
    private static AiServiceClient CreateClient(Mock<HttpMessageHandler> handlerMock)
    {
        var httpClient = new HttpClient(handlerMock.Object)
        {
            BaseAddress = new Uri("http://localhost:8000"),
        };
        return new AiServiceClient(httpClient);
    }

    [Fact]
    public async Task AskAsync_ReturnsResponse_WhenApiCallSucceeds()
    {
        // Arrange
        var expectedResponse = new NlqResponseDto("You spent $89.50 on shopping in January.", []);
        var handlerMock = new Mock<HttpMessageHandler>();

        handlerMock.Protected()
            .Setup<Task<HttpResponseMessage>>(
                "SendAsync",
                ItExpr.IsAny<HttpRequestMessage>(),
                ItExpr.IsAny<CancellationToken>())
            .ReturnsAsync(new HttpResponseMessage
            {
                StatusCode = HttpStatusCode.OK,
                Content = JsonContent.Create(expectedResponse),
            });

        var client = CreateClient(handlerMock);

        // Act
        var result = await client.AskAsync(new NlqRequestDto("How much did we spend on shopping?"));

        // Assert
        Assert.Equal(expectedResponse.Answer, result.Answer);
        Assert.Equal(expectedResponse.Data, result.Data);
    }

    [Fact]
    public async Task AskAsync_ThrowsAiServiceUnavailableException_WhenHttpRequestFails()
    {
        // Arrange
        var handlerMock = new Mock<HttpMessageHandler>();

        handlerMock.Protected()
            .Setup<Task<HttpResponseMessage>>(
                "SendAsync",
                ItExpr.IsAny<HttpRequestMessage>(),
                ItExpr.IsAny<CancellationToken>())
            .ThrowsAsync(new HttpRequestException("Connection refused"));

        var client = CreateClient(handlerMock);

        // Act & Assert
        await Assert.ThrowsAsync<AiServiceUnavailableException>(
            () => client.AskAsync(new NlqRequestDto("How much did we spend?")));
    }

    [Fact]
    public async Task AskAsync_ThrowsAiServiceUnavailableException_WhenServerReturnsError()
    {
        // Arrange
        var handlerMock = new Mock<HttpMessageHandler>();

        handlerMock.Protected()
            .Setup<Task<HttpResponseMessage>>(
                "SendAsync",
                ItExpr.IsAny<HttpRequestMessage>(),
                ItExpr.IsAny<CancellationToken>())
            .ReturnsAsync(new HttpResponseMessage
            {
                StatusCode = HttpStatusCode.ServiceUnavailable,
            });

        var client = CreateClient(handlerMock);

        // Act & Assert
        await Assert.ThrowsAsync<AiServiceUnavailableException>(
            () => client.AskAsync(new NlqRequestDto("How much did we spend?")));
    }

    [Fact]
    public async Task AskAsync_SendsPostRequest_ToCorrectEndpoint()
    {
        // Arrange
        HttpRequestMessage? capturedRequest = null;
        var expectedResponse = new NlqResponseDto("Test answer.", []);
        var handlerMock = new Mock<HttpMessageHandler>();

        handlerMock.Protected()
            .Setup<Task<HttpResponseMessage>>(
                "SendAsync",
                ItExpr.IsAny<HttpRequestMessage>(),
                ItExpr.IsAny<CancellationToken>())
            .Callback<HttpRequestMessage, CancellationToken>((req, _) => capturedRequest = req)
            .ReturnsAsync(new HttpResponseMessage
            {
                StatusCode = HttpStatusCode.OK,
                Content = JsonContent.Create(expectedResponse),
            });

        var client = CreateClient(handlerMock);

        // Act
        await client.AskAsync(new NlqRequestDto("test question"));

        // Assert
        Assert.NotNull(capturedRequest);
        Assert.Equal(HttpMethod.Post, capturedRequest.Method);
        Assert.Equal("/nlq/ask", capturedRequest.RequestUri!.AbsolutePath);
    }
}
