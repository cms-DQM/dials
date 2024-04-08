const reverseCantorPairing = (pi, y) => {
  const w = Math.floor(0.5 * (Math.sqrt(8 * pi + 1) - 1))
  return w - y
}

export default reverseCantorPairing
