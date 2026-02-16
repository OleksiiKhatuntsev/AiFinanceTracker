using FamilyFinance.Domain.Entities;
using FamilyFinance.Domain.Exceptions;

namespace FamilyFinance.Tests.Domain.Entities;

public class TransactionTests
{
    [Fact]
    public void Constructor_ShouldCreateTransaction_WhenInputIsValid()
    {
        // Arrange
        var amount = 100.50m;
        var currency = "usd";
        var merchant = "Amazon";
        var date = DateTime.UtcNow;

        // Act
        var transaction = new Transaction(amount, currency, merchant, date);

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
        var amount = -10.00m;
        var currency = "USD";
        var merchant = "Test Merchant";
        var date = DateTime.UtcNow;

        // Act & Assert
        Assert.Throws<InvalidAmountException>(() => new Transaction(amount, currency, merchant, date));
    }

    [Theory]
    [InlineData("")]
    [InlineData(" ")]
    [InlineData(null)]
    public void Constructor_ShouldThrowEmptyCurrencyException_WhenCurrencyIsInvalid(string? invalidCurrency)
    {
        // Arrange
        var amount = 100.00m;
        var merchant = "Test Merchant";
        var date = DateTime.UtcNow;

        // Act & Assert
        Assert.Throws<EmptyCurrencyException>(() => new Transaction(amount, invalidCurrency!, merchant, date));
    }

    [Theory]
    [InlineData("")]
    [InlineData(" ")]
    [InlineData(null)]
    public void Constructor_ShouldThrowArgumentNullException_WhenMerchantIsInvalid(string? invalidMerchant)
    {
        // Arrange
        var amount = 100.00m;
        var currency = "USD";
        var date = DateTime.UtcNow;

        // Act & Assert
        var exception = Assert.Throws<ArgumentNullException>(() => new Transaction(amount, currency, invalidMerchant!, date));
        Assert.Equal("merchant", exception.ParamName);
    }
}
