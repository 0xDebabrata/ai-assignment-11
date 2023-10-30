const Diseases = ({ diseases }: { diseases: string[] }) => {
  return diseases.length ? (
    <div>
      <h3>possible diseases:</h3>
      <ul className="card">
        {diseases.map((d) => (
          <li key={d} className="disease">
            {d}
          </li>
        ))}
      </ul>
    </div>
  ) : (
    <h3
      className="text-xl py-2 text-red-600"
    >
      sorry, we cannot match any of your symptoms to a disease in our knowledge base.
    </h3>
  );
};

export default Diseases;
