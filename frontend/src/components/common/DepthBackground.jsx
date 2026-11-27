// Decorative floating orbs placed behind all content.
// They have no content and ignore mouse clicks.
function DepthBackground() {
  return (
    <div aria-hidden="true">
      <div className="depth-orb depth-orb-one" />
      <div className="depth-orb depth-orb-two" />
      <div className="depth-orb depth-orb-three" />
    </div>
  );
}

export default DepthBackground;