using FamilyFinance.Application.Dto;
using FamilyFinance.Application.Mappings;
using FamilyFinance.Domain.Entities;

namespace FamilyFinance.Tests.Application.Mappings
{
    public class TransactionMappingTests
    {
        [Fact]
        public void ToDto_ShouldMapTransaction_Correctly()
        {
            // Arrange
            decimal amount = 100.50m;
            string currency = "USD";
            string merchant = "Amazon";
            DateTime date = DateTime.UtcNow;
            Transaction transaction = new(amount, currency, merchant, date);

            // Act
            TransactionDto dto = transaction.ToDto();

            // Assert
            Assert.Equal(transaction.Id, dto.Id);
            Assert.Equal(amount, dto.Amount);
            Assert.Equal(currency, dto.Currency);
            Assert.Equal(merchant, dto.Merchant);
            Assert.Equal(date, dto.Date);
            Assert.Equal("Uncategorized", dto.Category);
            Assert.Equal($"{amount:F2} {currency}", dto.FormattedAmount);
        }

        [Fact]
        public void ToEntity_ShouldMapTransactionDto_Correctly()
        {
            // Arrange
            decimal amount = 200.00m;
            string currency = "EUR";
            string merchant = "Supermarket";
            DateTime date = DateTime.UtcNow;
            TransactionDto dto = new(
                Guid.NewGuid(),
                amount,
                currency,
                merchant,
                date,
                "Groceries",
                "200.00 EUR"
            );

            // Act
            Transaction result = dto.ToEntity();

            // Assert
            Assert.NotEqual(Guid.Empty, result.Id);
            Assert.Equal(amount, result.Amount);
            Assert.Equal(currency, result.Currency);
            Assert.Equal(merchant, result.Merchant);
            Assert.Equal(date, result.Date);
        }
    }
}
