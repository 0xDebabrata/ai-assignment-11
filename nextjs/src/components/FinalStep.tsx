const Diseases = ({ diseases }: { diseases: string[] }) => {
  return diseases.length ? (
    <>
      <p className="underline my-5">
        possible diseases
      </p>
      <div className="max-w-xl flex flex-wrap">
          {diseases.map((d) => (
            <div key={d} className="rounded-full mx-2 my-2 py-1 px-3 bg-red-200 text-sm border border-red-500">
              {d}
            </div>
          ))}
      </div>
    </>
  ) : (
    <h3
      className="text-xl py-2 text-red-600"
    >
      sorry, we cannot match any of your symptoms to a disease in our knowledge base.
    </h3>
  );
};

export default Diseases;
