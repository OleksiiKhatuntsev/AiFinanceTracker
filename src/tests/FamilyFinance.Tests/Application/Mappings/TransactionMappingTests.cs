using FamilyFinance.Application.Mappings;
using FamilyFinance.Domain.Entities;

namespace FamilyFinance.Tests.Application;

public class TransactionMappingTests
{
    [Fact]
    public void ToDto_ShouldMapTransaction_Correctly()
    {
        // Arrange
        var amount = 100.50m;
        var currency = "USD";
        var merchant = "Amazon";
        var date = DateTime.UtcNow;
        var transaction = new Transaction(amount, currency, merchant, date);

        // Act
        var dto = transaction.ToDto();

        // Assert
        Assert.Equal(transaction.Id, dto.Id);
        Assert.Equal(amount, dto.Amount);
        Assert.Equal(currency, dto.Currency);
        Assert.Equal(merchant, dto.Merchant);
        Assert.Equal(date, dto.Date);
        Assert.Equal("Uncategorized", dto.Category);
        Assert.Equal($"{amount:F2} {currency}", dto.FormattedAmount);
    }
}
