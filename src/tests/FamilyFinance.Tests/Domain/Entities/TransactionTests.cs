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
            string category = "Shopping";

            // Act
            Transaction transaction = new(amount, currency, merchant, date, category);

            // Assert
            Assert.NotEqual(Guid.Empty, transaction.Id);
            Assert.Equal(amount, transaction.Amount);
            Assert.Equal("USD", transaction.Currency); // Verify currency is uppercased
            Assert.Equal(merchant, transaction.Merchant);
            Assert.Equal(date, transaction.Date);
            Assert.Equal(category, transaction.Category);
        }

        [Fact]
        public void Constructor_ShouldThrowInvalidAmountException_WhenAmountIsNegative()
        {
            // Arrange
            decimal amount = -10.00m;
            string currency = "USD";
            string merchant = "Test Merchant";
            DateTime date = DateTime.UtcNow;
            string category = "Shopping";

            // Act & Assert
            _ = Assert.Throws<InvalidAmountException>(() => new Transaction(amount, currency, merchant, date, category));
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
            string category = "Shopping";

            // Act & Assert
            _ = Assert.Throws<EmptyCurrencyException>(() => new Transaction(amount, invalidCurrency!, merchant, date, category));
        }

        [Theory]
        [InlineData("")]
        [InlineData(" ")]
        [InlineData(null)]
        public void Constructor_ShouldThrowEmptyMerchantException_WhenMerchantIsInvalid(string? invalidMerchant)
        {
            // Arrange
            decimal amount = 100.00m;
            string currency = "USD";
            DateTime date = DateTime.UtcNow;
            string category = "Shopping";

            // Act & Assert
            EmptyMerchantException exception = Assert.Throws<EmptyMerchantException>(() => new Transaction(amount, currency, invalidMerchant!, date, category));
            Assert.Equal("Merchant name is required and cannot be empty.", exception.Message);
        }

        [Theory]
        [InlineData("")]
        [InlineData(" ")]
        [InlineData(null)]
        public void Constructor_ShouldThrowEmptyCategoryException_WhenCategoryIsInvalid(string? invalidCategory)
        {
            // Arrange
            decimal amount = 100.00m;
            string currency = "USD";
            string merchant = "Test Merchant";
            DateTime date = DateTime.UtcNow;

            // Act & Assert
            EmptyCategoryException exception = Assert.Throws<EmptyCategoryException>(() => new Transaction(amount, currency, merchant, date, invalidCategory!));
            Assert.Equal("Category is required and cannot be empty.", exception.Message);
        }
    }
}
