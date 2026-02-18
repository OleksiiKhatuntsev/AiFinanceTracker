using FamilyFinance.Api.Controllers;
using FamilyFinance.Application.Dto;
using FamilyFinance.Domain.Entities;
using FamilyFinance.Domain.Repositories;
using Microsoft.AspNetCore.Mvc;
using Moq;

namespace FamilyFinance.Tests.Api.Controllers
{
    public class TransactionsControllerTests
    {
        [Fact]
        public void GetRandom_ShouldReturnOkResultWithTransactions()
        {
            // Arrange
            Mock<ITransactionRepository> mockRepository = new();
            List<Transaction> transactions =
            [
                new(100.00m, "USD", "Amazon", DateTime.UtcNow, "Web"),
                new(20.00m, "EUR", "Netflix", DateTime.UtcNow, "Web")
            ];

            _ = mockRepository.Setup(static repo => repo.GetAll()).Returns(transactions.AsReadOnly());

            TransactionsController controller = new(mockRepository.Object);

            // Act
            ActionResult<IEnumerable<TransactionDto>> result = controller.GetRandom();

            // Assert
            OkObjectResult okResult = Assert.IsType<OkObjectResult>(result.Result);
            IEnumerable<TransactionDto> returnedTransactions = Assert.IsType<IEnumerable<TransactionDto>>(okResult.Value, exactMatch: false);
            Assert.Equal(2, returnedTransactions.Count());
        }
    }
}
