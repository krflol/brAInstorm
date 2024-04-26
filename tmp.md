To restrict the DatePicker to only allow selecting Thursdays, you can use the `filterDate` prop and provide a custom function that checks if a given date is a Thursday. Here's how you can modify the DatePicker component in your code:

```jsx
<LocalizationProvider dateAdapter={AdapterDateFns}>
  <DatePicker
    label="Select Date (Thursdays only)"
    value={selectedDate}
    onChange={handleDateChange}
    filterDate={isThursday}
    renderInput={(params) => <TextField {...params} fullWidth />}
  />
</LocalizationProvider>
```

In the above code, we added the `filterDate` prop to the `DatePicker` component and passed the `isThursday` function to it.

Now, let's define the `isThursday` function:

```javascript
const isThursday = (date) => {
  const day = date.getDay();
  return day === 4;
};
```

The `isThursday` function takes a `date` parameter and checks if the day of the week is equal to 4 (Thursday). In JavaScript, days of the week are represented by numbers from 0 to 6, where 0 is Sunday, 1 is Monday, and so on. Thursday is represented by the number 4.

By passing the `isThursday` function to the `filterDate` prop, the DatePicker will only allow selecting dates that satisfy the condition defined in the function. In this case, it will only allow selecting Thursdays.

Make sure to define the `isThursday` function within your component or import it from another file if you have defined it elsewhere.

With these changes, the DatePicker will only allow users to select Thursdays, and any other dates will be disabled.