using FamilyFinance.Domain.Entities;
using FamilyFinance.Domain.Exceptions;

namespace FamilyFinance.Tests.Domain.Entities
{
    public class TransactionTests
    {
        [Fact]
        public void Constructor_ShouldCreateTransaction_WhenInputIsValid()
        {
            // Arrange
            decimal amount = 100.50m;
            string currency = "usd";
            string merchant = "Amazon";
            DateTime date = DateTime.UtcNow;

            // Act
            Transaction transaction = new(amount, currency, merchant, date);

            // Assert
            Assert.NotEqual(Guid.Empty, transaction.Id);
            Assert.Equal(amount, transaction.Amount);
            Assert.Equal("USD", transaction.Currency); // Verify currency is uppercased
            Assert.Equal(merchant, transaction.Merchant);
            Assert.Equal(date, transaction.Date);
        }

        [Fact]
        public void Constructor_ShouldThrowInvalidAmountException_WhenAmountIsNegative()
        {
            // Arrange
            decimal amount = -10.00m;
            string currency = "USD";
            string merchant = "Test Merchant";
            DateTime date = DateTime.UtcNow;

            // Act & Assert
            _ = Assert.Throws<InvalidAmountException>(() => new Transaction(amount, currency, merchant, date));
        }

        [Theory]
        [InlineData("")]
        [InlineData(" ")]
        [InlineData(null)]
        public void Constructor_ShouldThrowEmptyCurrencyException_WhenCurrencyIsInvalid(string? invalidCurrency)
        {
            // Arrange
            decimal amount = 100.00m;
            string merchant = "Test Merchant";
            DateTime date = DateTime.UtcNow;

            // Act & Assert
            _ = Assert.Throws<EmptyCurrencyException>(() => new Transaction(amount, invalidCurrency!, merchant, date));
        }

        [Theory]
        [InlineData("")]
        [InlineData(" ")]
        [InlineData(null)]
        public void Constructor_ShouldThrowArgumentNullException_WhenMerchantIsInvalid(string? invalidMerchant)
        {
            // Arrange
            decimal amount = 100.00m;
            string currency = "USD";
            DateTime date = DateTime.UtcNow;

            // Act & Assert
            EmptyMerchantException exception = Assert.Throws<EmptyMerchantException>(() => new Transaction(amount, currency, invalidMerchant!, date));
            Assert.Equal("Merchant name is required and cannot be empty.", exception.Message);
        }
    }
}
